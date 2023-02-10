from typing import Optional

from reqif.models.reqif_spec_object_type import ReqIFSpecObjectType
from reqif.parser import ReqIFParser


def test_01_get_spec_object_type_by_ref():
    reqif = """
<?xml version="1.0" encoding="UTF-8"?>
<REQ-IF
  xmlns="http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
  xmlns:configuration="http://eclipse.org/rmf/pror/toolextensions/1.0"
>
  <CORE-CONTENT>
    <REQ-IF-CONTENT>
      <SPEC-TYPES>
        <SPEC-OBJECT-TYPE IDENTIFIER="TEST_SPEC_OBJECT_TYPE_IDENTIFIER_FUNCTIONAL" LAST-CHANGE="2021-10-15T08:59:33.583+02:00" LONG-NAME="technical">
          <SPEC-ATTRIBUTES>
            <ATTRIBUTE-DEFINITION-STRING IDENTIFIER="UID" LAST-CHANGE="2021-10-15T09:00:45.839+02:00" LONG-NAME="requirement_ID">
              <TYPE>
                <DATATYPE-DEFINITION-STRING-REF>TEST_DATATYPE_IDENTIFIER</DATATYPE-DEFINITION-STRING-REF>
              </TYPE>
            </ATTRIBUTE-DEFINITION-STRING>
          </SPEC-ATTRIBUTES>
        </SPEC-OBJECT-TYPE>
      </SPEC-TYPES>
    </REQ-IF-CONTENT>
  </CORE-CONTENT>
</REQ-IF>
""".strip()  # noqa: E501

    parser = ReqIFParser()
    bundle = parser.parse_from_string(reqif)

    spec_object_type_or_none: Optional[
        ReqIFSpecObjectType
    ] = bundle.get_spec_object_type_by_ref(
        "TEST_SPEC_OBJECT_TYPE_IDENTIFIER_FUNCTIONAL"
    )
    assert spec_object_type_or_none is not None
    assert (
        spec_object_type_or_none.identifier
        == "TEST_SPEC_OBJECT_TYPE_IDENTIFIER_FUNCTIONAL"
    )
