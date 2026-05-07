from lxml import etree

from reqif.models.reqif_specification_type import ReqIFSpecificationType
from reqif.parsers.spec_types.specification_type_parser import (
    SpecificationTypeParser,
)


def test_02_default_value_survives_unparse() -> None:
    spec_type_string = """\
        <SPECIFICATION-TYPE IDENTIFIER="ST_ID" LAST-CHANGE="2015-12-14T02:04:51.769+01:00" LONG-NAME="ST">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="_attr_title" LAST-CHANGE="2015-12-14T02:04:51.769+01:00" LONG-NAME="Title">
              <DEFAULT-VALUE>
                <ATTRIBUTE-VALUE-STRING THE-VALUE="Untitled"/>
              </DEFAULT-VALUE>
              <TYPE>
                <DATATYPE-DEFINITION-STRING-REF>_dtype_String</DATATYPE-DEFINITION-STRING-REF>
              </TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
          </SPEC-ATTRIBUTES>
        </SPECIFICATION-TYPE>"""
    xml = etree.fromstring(spec_type_string)
    result = SpecificationTypeParser.parse(xml)
    assert result.spec_attributes is not None
    assert result.spec_attributes[0].default_value == "Untitled"

    unparsed = SpecificationTypeParser.unparse(result)
    assert "DEFAULT-VALUE" in unparsed
    assert "Untitled" in unparsed


def test_01_nominal_case() -> None:
    spec_type_string = """
        <SPECIFICATION-TYPE IDENTIFIER="TEST_SPECIFICATION_TYPE_ID" LAST-CHANGE="2015-12-14T02:04:51.769+01:00" LONG-NAME="TEST_SPECIFICATION_TYPE_LONG_NAME">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="TEST_SPEC_ATTRIBUTE_ID" LAST-CHANGE="2015-12-14T02:04:51.769+01:00" LONG-NAME="TEST_SPEC_ATTRIBUTE_LONG_NAME">
              <TYPE>
                <DATATYPE-DEFINITION-STRING-REF>_dtype_String</DATATYPE-DEFINITION-STRING-REF>
              </TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
          </SPEC-ATTRIBUTES>
        </SPECIFICATION-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_specification_type = SpecificationTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_specification_type, ReqIFSpecificationType)
    assert reqif_specification_type.identifier == "TEST_SPECIFICATION_TYPE_ID"
    assert reqif_specification_type.long_name == "TEST_SPECIFICATION_TYPE_LONG_NAME"
    attribute_map = reqif_specification_type.spec_attribute_map
    assert len(attribute_map) == 1
    assert (
        attribute_map.get("TEST_SPEC_ATTRIBUTE_ID") == "TEST_SPEC_ATTRIBUTE_LONG_NAME"
    )
