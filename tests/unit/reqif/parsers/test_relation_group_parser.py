import logging
from xml.etree import ElementTree

import pytest

from reqif.parsers.relation_group_parser import (
    ReqIFRelationGroupParser,
)

RELATION_GROUP_WITH_VALUES = """
<RELATION-GROUP IDENTIFIER="TEST_RELATION_GROUP_ID">
  <VALUES>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="String value">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>DEF_STRING</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
    <ATTRIBUTE-VALUE-INTEGER THE-VALUE="42">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-INTEGER-REF>DEF_INTEGER</ATTRIBUTE-DEFINITION-INTEGER-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-INTEGER>
  </VALUES>
  <TYPE>
    <RELATION-GROUP-TYPE-REF>TEST_RELATION_GROUP_TYPE_ID</RELATION-GROUP-TYPE-REF>
  </TYPE>
</RELATION-GROUP>
"""  # noqa: E501


def test_01_nominal_case() -> None:
    relation_group_string = """
<RELATION-GROUP IDENTIFIER="TEST_RELATION_GROUP_ID" LONG-NAME="Relation group">
  <SPEC-RELATIONS>
    <SPEC-RELATION-REF>TEST_SPEC_RELATION_ID</SPEC-RELATION-REF>
  </SPEC-RELATIONS>
  <TYPE>
    <RELATION-GROUP-TYPE-REF>TEST_RELATION_GROUP_TYPE_ID</RELATION-GROUP-TYPE-REF>
  </TYPE>
  <SOURCE-SPECIFICATION>
    <SPECIFICATION-REF>SPECIFICATION_A</SPECIFICATION-REF>
  </SOURCE-SPECIFICATION>
  <TARGET-SPECIFICATION>
    <SPECIFICATION-REF>SPECIFICATION_B</SPECIFICATION-REF>
  </TARGET-SPECIFICATION>
</RELATION-GROUP>
    """  # noqa: E501

    relation_group_xml = ElementTree.fromstring(relation_group_string)
    relation_group = ReqIFRelationGroupParser.parse(relation_group_xml)
    assert relation_group.identifier == "TEST_RELATION_GROUP_ID"
    assert relation_group.spec_relations == ["TEST_SPEC_RELATION_ID"]
    assert relation_group.values is None

    # A RELATION-GROUP without VALUES must not grow one on unparse.
    assert "VALUES" not in ReqIFRelationGroupParser.unparse(relation_group)


def test_02_attribute_values_survive_round_trip() -> None:
    relation_group_xml = ElementTree.fromstring(RELATION_GROUP_WITH_VALUES)
    relation_group = ReqIFRelationGroupParser.parse(relation_group_xml)

    assert relation_group.values is not None
    assert len(relation_group.values) == 2
    assert [value.definition_ref for value in relation_group.values] == [
        "DEF_STRING",
        "DEF_INTEGER",
    ]
    assert [value.value for value in relation_group.values] == ["String value", "42"]

    unparsed = ReqIFRelationGroupParser.unparse(relation_group)
    assert "DEF_STRING" in unparsed
    assert "DEF_INTEGER" in unparsed
    # VALUES is emitted first, as SPEC-OBJECT does. RELATION-GROUP is an
    # xsd:all, so child order carries no meaning; this just pins the output.
    assert unparsed.index("<VALUES>") < unparsed.index("<TYPE>")


LOGGER_NAME = "reqif.parsers.relation_group_parser"


def test_03_writing_values_warns_once_per_group(
    caplog: pytest.LogCaptureFixture,
) -> None:
    relation_group = ReqIFRelationGroupParser.parse(
        ElementTree.fromstring(RELATION_GROUP_WITH_VALUES)
    )

    # Parsing is silent: importing tools should be forgiving about what they read.
    assert caplog.records == []

    with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
        ReqIFRelationGroupParser.unparse(relation_group)

    # One warning for the group, naming it, whatever the number of values.
    warnings = [
        record for record in caplog.records if record.levelno == logging.WARNING
    ]
    assert len(warnings) == 1
    message = warnings[0].getMessage()
    assert "TEST_RELATION_GROUP_ID" in message
    assert "2.11" in message


def test_04_no_warning_without_values(caplog: pytest.LogCaptureFixture) -> None:
    relation_group_string = """
<RELATION-GROUP IDENTIFIER="TEST_RELATION_GROUP_ID">
  <TYPE>
    <RELATION-GROUP-TYPE-REF>TEST_RELATION_GROUP_TYPE_ID</RELATION-GROUP-TYPE-REF>
  </TYPE>
</RELATION-GROUP>
    """  # noqa: E501

    relation_group = ReqIFRelationGroupParser.parse(
        ElementTree.fromstring(relation_group_string)
    )
    with caplog.at_level(logging.WARNING, logger=LOGGER_NAME):
        ReqIFRelationGroupParser.unparse(relation_group)
    assert caplog.records == []


def test_05_warning_is_suppressible(caplog: pytest.LogCaptureFixture) -> None:
    """A caller who has decided to write these values can silence the warning
    through the standard logging hierarchy, without any reqif-specific API."""
    relation_group = ReqIFRelationGroupParser.parse(
        ElementTree.fromstring(RELATION_GROUP_WITH_VALUES)
    )

    logger = logging.getLogger(LOGGER_NAME)
    original_level = logger.level
    logger.setLevel(logging.ERROR)
    try:
        unparsed = ReqIFRelationGroupParser.unparse(relation_group)
    finally:
        logger.setLevel(original_level)

    # Warning suppressed, output unchanged.
    assert caplog.records == []
    assert "<VALUES>" in unparsed
