from lxml import etree

from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
)
from reqif.parsers.spec_types.spec_object_type_parser import (
    SpecObjectTypeParser,
)


def test_01_nominal_case() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="_gFhrW2ojEeuExICsU7Acmg" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="ReqIF.ForeignID">
      <TYPE>
        <DATATYPE-DEFINITION-STRING-REF>_gFhrVGojEeuExICsU7Acmg</DATATYPE-DEFINITION-STRING-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-STRING>
    <ATTRIBUTE-DEFINITION-STRING DESC="Testattribute" IDENTIFIER="_aqZG4GxpEeuaU7fHySy8Bw" IS-EDITABLE="true" LAST-CHANGE="2021-02-11T14:02:05.129+01:00" LONG-NAME="NOTES">
      <TYPE>
        <DATATYPE-DEFINITION-STRING-REF>_gFhrU2ojEeuExICsU7Acmg</DATATYPE-DEFINITION-STRING-REF>
      </TYPE>
      <DEFAULT-VALUE/>
    </ATTRIBUTE-DEFINITION-STRING>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert len(attribute_map) == 2
    assert (
        attribute_map.get("_gFhrW2ojEeuExICsU7Acmg").long_name
        == "ReqIF.ForeignID"
    )
    assert attribute_map.get("_aqZG4GxpEeuaU7fHySy8Bw").long_name == "NOTES"


def test_02_integer_attribute_definition() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-INTEGER IDENTIFIER="TEST_INTEGER_ATTRIBUTE_ID" LONG-NAME="IntegerAttributeId" IS-EDITABLE="false">
      <TYPE>
        <DATATYPE-DEFINITION-INTEGER-REF>TEST_INTEGER_TYPE</DATATYPE-DEFINITION-INTEGER-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-INTEGER>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert len(attribute_map) == 1
    assert (
        attribute_map.get("TEST_INTEGER_ATTRIBUTE_ID").long_name
        == "IntegerAttributeId"
    )


def test_03_boolean_attribute_definition() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-BOOLEAN IDENTIFIER="TEST_BOOLEAN_ATTRIBUTE_ID" IS-EDITABLE="true" LAST-CHANGE="2015-12-14T02:04:51.768+01:00" LONG-NAME="BooleanAttributeId">
      <TYPE>
        <DATATYPE-DEFINITION-BOOLEAN-REF>TEST_BOOLEAN_TYPE</DATATYPE-DEFINITION-BOOLEAN-REF>
      </TYPE>
      <DEFAULT-VALUE>
        <ATTRIBUTE-VALUE-BOOLEAN THE-VALUE="false">
          <DEFINITION>
            <ATTRIBUTE-DEFINITION-BOOLEAN-REF>_stype_requirement_atomic</ATTRIBUTE-DEFINITION-BOOLEAN-REF>
          </DEFINITION>
        </ATTRIBUTE-VALUE-BOOLEAN>
      </DEFAULT-VALUE>
    </ATTRIBUTE-DEFINITION-BOOLEAN>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert len(attribute_map) == 1
    assert (
        attribute_map.get("TEST_BOOLEAN_ATTRIBUTE_ID").long_name
        == "BooleanAttributeId"
    )


def test_04_xhtml_attribute_definition() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-XHTML IDENTIFIER="TEST_XHTML_ATTRIBUTE_ID" IS-EDITABLE="false" LAST-CHANGE="2015-12-14T02:04:51.768+01:00" LONG-NAME="TEST_XHTML_ATTRIBUTE_LONG_NAME">
      <TYPE>
        <DATATYPE-DEFINITION-XHTML-REF>TEST_XHTML_ATTRIBUTE_DATATYPE_REF</DATATYPE-DEFINITION-XHTML-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-XHTML>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert (
        attribute_map.get("TEST_XHTML_ATTRIBUTE_ID").long_name
        == "TEST_XHTML_ATTRIBUTE_LONG_NAME"
    )


def test_05_enumeration_attribute_definition() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2021-02-08T16:37:07.454+01:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
   <ATTRIBUTE-DEFINITION-ENUMERATION IDENTIFIER="TEST_ENUMERATION_ATTRIBUTE_ID" IS-EDITABLE="true" LAST-CHANGE="2015-12-14T02:04:51.768+01:00" LONG-NAME="TEST_ENUMERATION_ATTRIBUTE_LONG_NAME" MULTI-VALUED="false">
      <TYPE>
        <DATATYPE-DEFINITION-ENUMERATION-REF>TEST_ENUMERATION_ATTRIBUTE_DATATYPE_REF</DATATYPE-DEFINITION-ENUMERATION-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-ENUMERATION>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert (
        attribute_map.get("TEST_ENUMERATION_ATTRIBUTE_ID").long_name
        == "TEST_ENUMERATION_ATTRIBUTE_LONG_NAME"
    )


def test_06_string_attribute_default_value() -> None:
    spec_type_string = """
<SPEC-OBJECT-TYPE DESC="Description goes here" IDENTIFIER="TEST_SPEC_OBJECT_TYPE_ID" LAST-CHANGE="2005-05-30T11:42:19+02:00" LONG-NAME="TEST_SPEC_OBJECT_TYPE_LONG_NAME">
  <SPEC-ATTRIBUTES>
    <ATTRIBUTE-DEFINITION-STRING DESC="This attribute contains the author of the requirement as a string." IDENTIFIER="TEST_STRING_ATTRIBUTE_ID" LAST-CHANGE="2005-05-30T11:51:25+02:00" LONG-NAME="TEST_STRING_ATTRIBUTE_LONG_NAME">
      <DEFAULT-VALUE>
        <ATTRIBUTE-VALUE-STRING THE-VALUE="TBD"/>
      </DEFAULT-VALUE>
      <TYPE>
        <DATATYPE-DEFINITION-STRING-REF>3631dcd2-59d1-11da-beb2-6fbc179f63e3</DATATYPE-DEFINITION-STRING-REF>
      </TYPE>
    </ATTRIBUTE-DEFINITION-STRING>
  </SPEC-ATTRIBUTES>
</SPEC-OBJECT-TYPE>
    """  # noqa: E501
    spec_type_xml = etree.fromstring(spec_type_string)

    reqif_spec_object_type = SpecObjectTypeParser.parse(spec_type_xml)
    assert isinstance(reqif_spec_object_type, ReqIFSpecObjectType)
    assert reqif_spec_object_type.identifier == "TEST_SPEC_OBJECT_TYPE_ID"
    assert reqif_spec_object_type.long_name == "TEST_SPEC_OBJECT_TYPE_LONG_NAME"
    attribute_map = reqif_spec_object_type.attribute_map
    assert (
        attribute_map.get("TEST_STRING_ATTRIBUTE_ID").long_name
        == "TEST_STRING_ATTRIBUTE_LONG_NAME"
    )
    assert (
        reqif_spec_object_type.attribute_definitions[0].default_value == "TBD"
    )
