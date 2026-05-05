from lxml import etree

from reqif.models.reqif_relation_group_type import ReqIFRelationGroupType
from reqif.parsers.spec_types.relation_group_type_parser import RelationGroupTypeParser


def test_01_no_spec_attributes() -> None:
    xml = etree.fromstring(
        '<RELATION-GROUP-TYPE IDENTIFIER="RGT_ID" LAST-CHANGE="2012-04-07T01:51:37.112+02:00" LONG-NAME="RGT"/>'
    )
    result = RelationGroupTypeParser.parse(xml)
    assert isinstance(result, ReqIFRelationGroupType)
    assert result.identifier == "RGT_ID"
    assert result.attribute_definitions is None


def test_02_spec_attributes_round_trip() -> None:
    xml_string = """\
<RELATION-GROUP-TYPE IDENTIFIER="RGT_ID" LAST-CHANGE="2012-04-07T01:51:37.112+02:00" LONG-NAME="RGT With Attrs">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="_attr_comment" LAST-CHANGE="2015-12-14T02:04:51.769+01:00" LONG-NAME="Comment">
      <TYPE>
        <DATATYPE-DEFINITION-STRING-REF>_dtype_String</DATATYPE-DEFINITION-STRING-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-STRING>
  </SPEC-ATTRIBUTES>
</RELATION-GROUP-TYPE>"""
    xml = etree.fromstring(xml_string)
    result = RelationGroupTypeParser.parse(xml)
    assert isinstance(result, ReqIFRelationGroupType)
    assert result.attribute_definitions is not None
    assert len(result.attribute_definitions) == 1
    assert result.attribute_definitions[0].identifier == "_attr_comment"
    assert result.attribute_definitions[0].long_name == "Comment"

    unparsed = RelationGroupTypeParser.unparse(result)
    assert "SPEC-ATTRIBUTES" in unparsed
    assert "_attr_comment" in unparsed
    assert "Comment" in unparsed
