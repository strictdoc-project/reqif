from reqif.parser import ReqIFParser


def test_01_normal_case():
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

    expected_stripped_xhtml = """\
<div>
  <p style=" font-style: italic">Delay <span style="text-decoration: underline;">&lt;= 5s</span></p>
</div>\
"""  # noqa: E501

    reqif_bundle = ReqIFParser.parse_from_string(input_reqif)
    spec_object = reqif_bundle.get_spec_object_by_ref(
        "TEST_SPEC_OBJECT_IDENTIFIER"
    )

    assert (
        spec_object.attribute_map[
            "_gFhrXWojEeuExICsU7Acmg"
        ].value_stripped_xhtml
        == expected_stripped_xhtml
    )


def test_02_edge_case_object_tag_no_xhtml_ns():
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
                  <object data="files/rmf-1b18ef37-ca1f-4e79-954d-747df083f861_DOCATTACHMENT_3-screenshot-20220926-051927.png" name="DOCATTACHMENT_3-screenshot-20220926-051927.png" type="image/png"/>
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

    expected_stripped_xhtml = """\
<div>
  <object data="files/rmf-1b18ef37-ca1f-4e79-954d-747df083f861_DOCATTACHMENT_3-screenshot-20220926-051927.png" name="DOCATTACHMENT_3-screenshot-20220926-051927.png" type="image/png"></object>
</div>\
"""  # noqa: E501

    reqif_bundle = ReqIFParser.parse_from_string(input_reqif)
    spec_object = reqif_bundle.get_spec_object_by_ref(
        "TEST_SPEC_OBJECT_IDENTIFIER"
    )

    assert (
        spec_object.attribute_map[
            "_gFhrXWojEeuExICsU7Acmg"
        ].value_stripped_xhtml
        == expected_stripped_xhtml
    )


def test_03_edge_case_object_tag_xhtml_ns():
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
                  <xhtml:object data="files/rmf-1b18ef37-ca1f-4e79-954d-747df083f861_DOCATTACHMENT_3-screenshot-20220926-051927.png" name="DOCATTACHMENT_3-screenshot-20220926-051927.png" type="image/png"/>
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

    expected_stripped_xhtml = """\
<div>
  <object data="files/rmf-1b18ef37-ca1f-4e79-954d-747df083f861_DOCATTACHMENT_3-screenshot-20220926-051927.png" name="DOCATTACHMENT_3-screenshot-20220926-051927.png" type="image/png"></object>
</div>\
"""  # noqa: E501

    reqif_bundle = ReqIFParser.parse_from_string(input_reqif)
    spec_object = reqif_bundle.get_spec_object_by_ref(
        "TEST_SPEC_OBJECT_IDENTIFIER"
    )

    assert (
        spec_object.attribute_map[
            "_gFhrXWojEeuExICsU7Acmg"
        ].value_stripped_xhtml
        == expected_stripped_xhtml
    )
