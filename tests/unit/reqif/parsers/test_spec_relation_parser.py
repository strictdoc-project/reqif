from xml.etree import ElementTree

from reqif.parsers.spec_relation_parser import (
    SpecRelationParser,
)


def test_01_nominal_case() -> None:
    spec_object_string = """
<SPEC-RELATION IDENTIFIER="TEST_SPEC_RELATION_ID" LAST-CHANGE="2015-12-14T02:04:52.318+01:00">
  <TARGET>
    <SPEC-OBJECT-REF>SPEC_OBJECT_B</SPEC-OBJECT-REF>
  </TARGET>
  <SOURCE>
    <SPEC-OBJECT-REF>SPEC_OBJECT_A</SPEC-OBJECT-REF>
  </SOURCE>
  <TYPE>
    <SPEC-RELATION-TYPE-REF>PARENT</SPEC-RELATION-TYPE-REF>
  </TYPE>
</SPEC-RELATION>
    """  # noqa: E501

    spec_object_xml = ElementTree.fromstring(spec_object_string)
    spec_object = SpecRelationParser.parse(spec_object_xml)
    assert spec_object.identifier == "TEST_SPEC_RELATION_ID"
    assert spec_object.relation_type_ref == "PARENT"
    assert spec_object.source == "SPEC_OBJECT_A"
    assert spec_object.target == "SPEC_OBJECT_B"
    assert spec_object.values is None
    assert spec_object.values_attribute is None


def test_02_multiple_attribute_values_survive_round_trip() -> None:
    spec_relation_string = """
<SPEC-RELATION IDENTIFIER="TEST_SPEC_RELATION_ID">
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
    <ATTRIBUTE-VALUE-BOOLEAN THE-VALUE="true">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-BOOLEAN-REF>DEF_BOOLEAN</ATTRIBUTE-DEFINITION-BOOLEAN-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-BOOLEAN>
  </VALUES>
  <TYPE>
    <SPEC-RELATION-TYPE-REF>PARENT</SPEC-RELATION-TYPE-REF>
  </TYPE>
  <SOURCE>
    <SPEC-OBJECT-REF>SPEC_OBJECT_A</SPEC-OBJECT-REF>
  </SOURCE>
  <TARGET>
    <SPEC-OBJECT-REF>SPEC_OBJECT_B</SPEC-OBJECT-REF>
  </TARGET>
</SPEC-RELATION>
    """  # noqa: E501

    spec_relation_xml = ElementTree.fromstring(spec_relation_string)
    spec_relation = SpecRelationParser.parse(spec_relation_xml)

    # All three values are kept. Previously only the first was parsed, and
    # BOOLEAN raised NotImplementedError.
    assert spec_relation.values is not None
    assert len(spec_relation.values) == 3
    assert [value.definition_ref for value in spec_relation.values] == [
        "DEF_STRING",
        "DEF_INTEGER",
        "DEF_BOOLEAN",
    ]
    # Values are kept as the raw strings from THE-VALUE, booleans included.
    assert [value.value for value in spec_relation.values] == [
        "String value",
        "42",
        "true",
    ]

    unparsed = SpecRelationParser.unparse(spec_relation)
    assert "DEF_STRING" in unparsed
    assert "DEF_INTEGER" in unparsed
    assert "DEF_BOOLEAN" in unparsed


def test_03_values_attribute_stays_backward_compatible() -> None:
    spec_relation_string = """
<SPEC-RELATION IDENTIFIER="TEST_SPEC_RELATION_ID">
  <VALUES>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="First">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>DEF_ONE</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="Second">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>DEF_TWO</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
  </VALUES>
  <TYPE>
    <SPEC-RELATION-TYPE-REF>PARENT</SPEC-RELATION-TYPE-REF>
  </TYPE>
  <SOURCE>
    <SPEC-OBJECT-REF>SPEC_OBJECT_A</SPEC-OBJECT-REF>
  </SOURCE>
  <TARGET>
    <SPEC-OBJECT-REF>SPEC_OBJECT_B</SPEC-OBJECT-REF>
  </TARGET>
</SPEC-RELATION>
    """  # noqa: E501

    spec_relation_xml = ElementTree.fromstring(spec_relation_string)
    spec_relation = SpecRelationParser.parse(spec_relation_xml)

    # The deprecated accessor still reads the first value.
    assert spec_relation.values_attribute is not None
    assert spec_relation.values_attribute.definition_ref == "DEF_ONE"

    # And writing through it still replaces the values wholesale.
    spec_relation.values_attribute = spec_relation.values[1]
    assert spec_relation.values is not None
    assert len(spec_relation.values) == 1
    assert spec_relation.values[0].definition_ref == "DEF_TWO"

    spec_relation.values_attribute = None
    assert spec_relation.values is None
