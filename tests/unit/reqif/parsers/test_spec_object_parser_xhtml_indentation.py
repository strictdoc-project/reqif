from reqif.helpers.string.xhtml_indent import reqif_indent_xhtml_string
from reqif.parser import ReqIFParser
from reqif.unparser import ReqIFUnparser


def test_01_indenting_unintended_xhtml():
    input_reqif = """\
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <CORE-CONTENT>
    <REQ-IF-CONTENT>
      <SPEC-OBJECTS>
        <SPEC-OBJECT IDENTIFIER="TEST_SPEC_OBJECT_IDENTIFIER" LAST-CHANGE="2021-10-15T11:34:36.007+02:00">
          <VALUES>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-XHTML-REF>_gFhrXWojEeuExICsU7Acmg</ATTRIBUTE-DEFINITION-XHTML-REF>
              </DEFINITION>
              <THE-VALUE>
                <xhtml:div>
                  <xhtml:p style=" font-style: italic">Delay <xhtml:span style="text-decoration: underline;">&lt;= 5s</xhtml:span></xhtml:p>
                </xhtml:div>
              </THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
          <TYPE>
            <SPEC-OBJECT-TYPE-REF>TEST_SPEC_OBJECT_TYPE_IDENTIFIER_FUNCTIONAL</SPEC-OBJECT-TYPE-REF>
          </TYPE>
        </SPEC-OBJECT>
      </SPEC-OBJECTS>
    </REQ-IF-CONTENT>
  </CORE-CONTENT>
</REQ-IF>
"""  # noqa: E501

    expected_reqif = """\
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd" xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <CORE-CONTENT>
    <REQ-IF-CONTENT>
      <SPEC-OBJECTS>
        <SPEC-OBJECT IDENTIFIER="TEST_SPEC_OBJECT_IDENTIFIER" LAST-CHANGE="2021-10-15T11:34:36.007+02:00">
          <VALUES>
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-XHTML-REF>_gFhrXWojEeuExICsU7Acmg</ATTRIBUTE-DEFINITION-XHTML-REF>
              </DEFINITION>
              <THE-VALUE>
                A
                  B
                    C
                  D
                E
              </THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
          </VALUES>
          <TYPE>
            <SPEC-OBJECT-TYPE-REF>TEST_SPEC_OBJECT_TYPE_IDENTIFIER_FUNCTIONAL</SPEC-OBJECT-TYPE-REF>
          </TYPE>
        </SPEC-OBJECT>
      </SPEC-OBJECTS>
    </REQ-IF-CONTENT>
  </CORE-CONTENT>
</REQ-IF>
"""  # noqa: E501

    reqif_bundle = ReqIFParser.parse_from_string(input_reqif)
    spec_object = reqif_bundle.get_spec_object_by_ref(
        "TEST_SPEC_OBJECT_IDENTIFIER"
    )

    multiline_text = reqif_indent_xhtml_string(
        """\
A
  B
    C
  D
E
"""
    )
    spec_object.attribute_map["_gFhrXWojEeuExICsU7Acmg"].value = multiline_text
    assert spec_object is not None

    unparsed_reqif = ReqIFUnparser.unparse(reqif_bundle)

    assert unparsed_reqif == expected_reqif
