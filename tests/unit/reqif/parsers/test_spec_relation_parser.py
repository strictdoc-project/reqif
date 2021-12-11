from xml.etree import ElementTree as etree

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

    spec_object_xml = etree.fromstring(spec_object_string)
    spec_object = SpecRelationParser.parse(spec_object_xml)
    assert spec_object.identifier == "TEST_SPEC_RELATION_ID"
    assert spec_object.relation_type_ref == "PARENT"
    assert spec_object.source == "SPEC_OBJECT_A"
    assert spec_object.target == "SPEC_OBJECT_B"
