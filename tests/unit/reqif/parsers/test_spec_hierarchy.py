from xml.etree import ElementTree

import pytest

from reqif.models.reqif_types import SpecObjectAttributeType
from reqif.parsers.spec_hierarchy_parser import (
    ReqIFSpecHierarchyParser,
)


def test_01_nominal_case() -> None:
    specification_string = """
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1" LAST-CHANGE="2015-12-14T02:04:51.856+01:00">
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
  <CHILDREN>
    <SPEC-HIERARCHY IDENTIFIER="LEVEL_1_1" LAST-CHANGE="2015-12-14T02:04:51.857+01:00">
      <OBJECT>
        <SPEC-OBJECT-REF>TEST_OBJECT_REF_1_1</SPEC-OBJECT-REF>
      </OBJECT>
      <CHILDREN>
        <SPEC-HIERARCHY IDENTIFIER="LEVEL_1_1_1" LAST-CHANGE="2015-12-14T02:04:52.271+01:00">
          <OBJECT>
            <SPEC-OBJECT-REF>TEST_OBJECT_REF_1_1_1</SPEC-OBJECT-REF>
          </OBJECT>
        </SPEC-HIERARCHY>
      </CHILDREN>
    </SPEC-HIERARCHY>
  </CHILDREN>
</SPEC-HIERARCHY>
    """  # noqa: E501

    specification_xml = ElementTree.fromstring(specification_string)
    specification_1 = ReqIFSpecHierarchyParser.parse(specification_xml)
    assert specification_1.identifier == "LEVEL_1"
    assert specification_1.spec_object == "TEST_OBJECT_REF_1"
    assert specification_1.level == 1
    assert len(specification_1.children) == 1

    specification_1_1 = specification_1.children[0]
    assert specification_1_1.identifier == "LEVEL_1_1"
    assert len(specification_1_1.children) == 1
    assert specification_1_1.level == 2

    specification_1_1_1 = specification_1_1.children[0]
    assert specification_1_1_1.identifier == "LEVEL_1_1_1"
    assert specification_1_1_1.children is None
    assert specification_1_1_1.level == 3
    assert specification_1.editable_atts is None

    # A SPEC-HIERARCHY without EDITABLE-ATTS must not grow one.
    assert "EDITABLE-ATTS" not in ReqIFSpecHierarchyParser.unparse(specification_1)


def test_02_desc() -> None:
    specification_string = """\
<SPEC-HIERARCHY DESC="Some &amp; description" IDENTIFIER="LEVEL_1" LAST-CHANGE="2015-12-14T02:04:51.856+01:00">
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
</SPEC-HIERARCHY>
"""  # noqa: E501

    specification_xml = ElementTree.fromstring(specification_string)
    spec_hierarchy = ReqIFSpecHierarchyParser.parse(specification_xml)
    assert spec_hierarchy.description == "Some & description"

    unparsed = ReqIFSpecHierarchyParser.unparse(spec_hierarchy)
    assert unparsed.splitlines()[0].lstrip() == (
        '<SPEC-HIERARCHY DESC="Some &amp; description" IDENTIFIER="LEVEL_1" '
        'LAST-CHANGE="2015-12-14T02:04:51.856+01:00">'
    )


def test_03_no_desc_is_not_emitted() -> None:
    specification_string = """\
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1">
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
</SPEC-HIERARCHY>
"""

    specification_xml = ElementTree.fromstring(specification_string)
    spec_hierarchy = ReqIFSpecHierarchyParser.parse(specification_xml)
    assert spec_hierarchy.description is None
    assert "DESC" not in ReqIFSpecHierarchyParser.unparse(spec_hierarchy)


def test_04_editable_atts() -> None:
    specification_string = """
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1">
  <EDITABLE-ATTS>
    <ATTRIBUTE-DEFINITION-STRING-REF>DEF_STRING</ATTRIBUTE-DEFINITION-STRING-REF>
    <ATTRIBUTE-DEFINITION-XHTML-REF>DEF_XHTML</ATTRIBUTE-DEFINITION-XHTML-REF>
  </EDITABLE-ATTS>
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
</SPEC-HIERARCHY>
    """  # noqa: E501

    spec_hierarchy = ReqIFSpecHierarchyParser.parse(
        ElementTree.fromstring(specification_string)
    )

    assert spec_hierarchy.editable_atts is not None
    assert [
        (att.attribute_type, att.definition_ref) for att in spec_hierarchy.editable_atts
    ] == [
        (SpecObjectAttributeType.STRING, "DEF_STRING"),
        (SpecObjectAttributeType.XHTML, "DEF_XHTML"),
    ]

    # The reference tag names the attribute type, so it has to be reproduced.
    unparsed = ReqIFSpecHierarchyParser.unparse(spec_hierarchy)
    assert (
        "<ATTRIBUTE-DEFINITION-STRING-REF>DEF_STRING</ATTRIBUTE-DEFINITION-STRING-REF>"
        in unparsed
    )
    assert (
        "<ATTRIBUTE-DEFINITION-XHTML-REF>DEF_XHTML</ATTRIBUTE-DEFINITION-XHTML-REF>"
        in unparsed
    )
    assert unparsed.index("<EDITABLE-ATTS>") < unparsed.index("<OBJECT>")


def test_05_editable_atts_does_not_swap_object_and_children() -> None:
    """An extra child must not be read as "not the OBJECT-then-CHILDREN shape"."""
    specification_string = """
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1">
  <EDITABLE-ATTS>
    <ATTRIBUTE-DEFINITION-STRING-REF>DEF_STRING</ATTRIBUTE-DEFINITION-STRING-REF>
  </EDITABLE-ATTS>
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
  <CHILDREN>
    <SPEC-HIERARCHY IDENTIFIER="LEVEL_1_1">
      <OBJECT>
        <SPEC-OBJECT-REF>TEST_OBJECT_REF_1_1</SPEC-OBJECT-REF>
      </OBJECT>
    </SPEC-HIERARCHY>
  </CHILDREN>
</SPEC-HIERARCHY>
    """  # noqa: E501

    spec_hierarchy = ReqIFSpecHierarchyParser.parse(
        ElementTree.fromstring(specification_string)
    )
    assert spec_hierarchy.ref_then_children_order is True

    unparsed = ReqIFSpecHierarchyParser.unparse(spec_hierarchy)
    assert unparsed.index("<OBJECT>") < unparsed.index("<CHILDREN>")


def test_06_empty_editable_atts_stays_self_closed() -> None:
    specification_string = """
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1">
  <EDITABLE-ATTS/>
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
</SPEC-HIERARCHY>
    """  # noqa: E501

    spec_hierarchy = ReqIFSpecHierarchyParser.parse(
        ElementTree.fromstring(specification_string)
    )
    assert spec_hierarchy.editable_atts == []
    assert "<EDITABLE-ATTS/>" in ReqIFSpecHierarchyParser.unparse(spec_hierarchy)


def test_07_unknown_editable_atts_ref_is_rejected() -> None:
    specification_string = """
<SPEC-HIERARCHY IDENTIFIER="LEVEL_1">
  <EDITABLE-ATTS>
    <SPEC-OBJECT-REF>NOT_AN_ATTRIBUTE_DEFINITION</SPEC-OBJECT-REF>
  </EDITABLE-ATTS>
  <OBJECT>
    <SPEC-OBJECT-REF>TEST_OBJECT_REF_1</SPEC-OBJECT-REF>
  </OBJECT>
</SPEC-HIERARCHY>
    """  # noqa: E501

    with pytest.raises(NotImplementedError):
        ReqIFSpecHierarchyParser.parse(ElementTree.fromstring(specification_string))
