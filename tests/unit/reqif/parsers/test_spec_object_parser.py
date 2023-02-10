from lxml import etree

from reqif.parsers.spec_object_parser import (
    SpecObjectParser,
)


def test_01_nominal_case():
    spec_object_string = """
<SPEC-OBJECT IDENTIFIER="TEST_SPEC_OBJECT_ID" LAST-CHANGE="2021-10-15T11:32:40.205+02:00">
  <VALUES>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="SR001">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>TEST_FIELD_UID</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="Draft">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>TEST_FIELD_STATUS</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
    <ATTRIBUTE-VALUE-STRING THE-VALUE="Test statement">
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-STRING-REF>TEST_FIELD_STATEMENT</ATTRIBUTE-DEFINITION-STRING-REF>
      </DEFINITION>
    </ATTRIBUTE-VALUE-STRING>
  </VALUES>
  <TYPE>
    <SPEC-OBJECT-TYPE-REF>TEST_SPEC_OBJECT_TYPE</SPEC-OBJECT-TYPE-REF>
  </TYPE>
</SPEC-OBJECT>
    """  # noqa: E501

    spec_object_xml = etree.fromstring(spec_object_string)
    spec_object = SpecObjectParser.parse(spec_object_xml)
    assert spec_object.identifier == "TEST_SPEC_OBJECT_ID"
    assert spec_object.spec_object_type == "TEST_SPEC_OBJECT_TYPE"
    assert spec_object.attribute_map["TEST_FIELD_UID"].value == "SR001"
    assert spec_object.attribute_map["TEST_FIELD_STATUS"].value == "Draft"
    assert (
        spec_object.attribute_map["TEST_FIELD_STATEMENT"].value
        == "Test statement"
    )


def test_02_attributes_xhtml():
    spec_object_string = """\
<SPEC-OBJECT xmlns:reqif-xhtml="http://www.w3.org/1999/xhtml" IDENTIFIER="TEST_SPEC_OBJECT_ID" LAST-CHANGE="2021-10-15T11:32:40.205+02:00">
  <VALUES>
    <ATTRIBUTE-VALUE-XHTML>
      <DEFINITION>
        <ATTRIBUTE-DEFINITION-XHTML-REF>_7f123ed4-98dd-4eed-b96a-edc8828963a8_CREATEDBY</ATTRIBUTE-DEFINITION-XHTML-REF>
      </DEFINITION>
      <THE-VALUE>
        <reqif-xhtml:div>susan</reqif-xhtml:div>
      </THE-VALUE>
    </ATTRIBUTE-VALUE-XHTML>
  </VALUES>
  <TYPE>
    <SPEC-OBJECT-TYPE-REF>TEST_SPEC_OBJECT_TYPE</SPEC-OBJECT-TYPE-REF>
  </TYPE>
</SPEC-OBJECT>
    """  # noqa: E501

    spec_object_xml = etree.fromstring(spec_object_string)
    assert spec_object_xml is not None
    spec_object = SpecObjectParser.parse(spec_object_xml)
    assert spec_object.identifier == "TEST_SPEC_OBJECT_ID"

    expected_xhtml = (
        "\n        <reqif-xhtml:div>susan</reqif-xhtml:div>\n      "
    )
    assert (
        spec_object.attribute_map[
            "_7f123ed4-98dd-4eed-b96a-edc8828963a8_CREATEDBY"
        ].value
        == expected_xhtml
    )
