from reqif.models.reqif_spec_object_type import ReqIFSpecObjectType
from reqif.models.reqif_spec_relation_type import ReqIFSpecRelationType
from reqif.parsers.data_type_parser import DataTypeParser
from reqif.parsers.header_parser import ReqIFHeaderParser
from reqif.parsers.spec_object_parser import SpecObjectParser
from reqif.parsers.spec_object_type_parser import SpecObjectTypeParser
from reqif.parsers.spec_relation_type_parser import SpecRelationTypeParser
from reqif.parsers.specification_parser import ReqIFSpecificationParser
from reqif.reqif_bundle import ReqIFBundle


class ReqIFWriter:
    @staticmethod
    def write(bundle: ReqIFBundle) -> str:
        reqif_xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        if bundle.namespace is not None and bundle.configuration is not None:
            reqif_xml_output += (
                f"<REQ-IF "
                f'xmlns="{bundle.namespace}" '
                f'xmlns:configuration="{bundle.configuration}">'
                "\n"
            )
        else:
            raise NotImplementedError

        if bundle.req_if_header is not None:
            reqif_xml_output += ReqIFHeaderParser.unparse(bundle.req_if_header)

        if bundle.core_content is not None:
            reqif_xml_output += "  <CORE-CONTENT>\n"
            reqif_content = bundle.core_content.req_if_content
            if reqif_content:
                reqif_xml_output += "    <REQ-IF-CONTENT>\n"

                if reqif_content.data_types is not None:
                    reqif_xml_output += "      <DATATYPES>\n"
                    for data_type in reqif_content.data_types:
                        reqif_xml_output += DataTypeParser.unparse(data_type)
                    reqif_xml_output += "      </DATATYPES>\n"

                if reqif_content.spec_types is not None:
                    reqif_xml_output += "      <SPEC-TYPES>\n"
                    for spec_type in reqif_content.spec_types:
                        if isinstance(spec_type, ReqIFSpecObjectType):
                            reqif_xml_output += SpecObjectTypeParser.unparse(
                                spec_type
                            )
                        elif isinstance(spec_type, ReqIFSpecRelationType):
                            reqif_xml_output += SpecRelationTypeParser.unparse(
                                spec_type
                            )

                    reqif_xml_output += "      </SPEC-TYPES>\n"

                if reqif_content.spec_objects is not None:
                    reqif_xml_output += "      <SPEC-OBJECTS>\n"

                    for spec_object in reqif_content.spec_objects:
                        reqif_xml_output += SpecObjectParser.unparse(
                            spec_object
                        )

                    reqif_xml_output += "      </SPEC-OBJECTS>\n"

                if reqif_content.spec_relations is not None:
                    reqif_xml_output += "      <SPEC-RELATIONS>\n"
                    reqif_xml_output += "      </SPEC-RELATIONS>\n"

                if reqif_content.specifications is not None:
                    reqif_xml_output += "      <SPECIFICATIONS>\n"

                    for specification in reqif_content.specifications:
                        reqif_xml_output += ReqIFSpecificationParser.unparse(
                            specification
                        )

                    reqif_xml_output += "      </SPECIFICATIONS>\n"

                reqif_xml_output += "    </REQ-IF-CONTENT>\n"
            reqif_xml_output += "  </CORE-CONTENT>\n"

        if bundle.tool_extensions_tag_exists:
            reqif_xml_output += "  <TOOL-EXTENSIONS>\n"
            reqif_xml_output += "  </TOOL-EXTENSIONS>\n"

        reqif_xml_output += "</REQ-IF>" "\n"
        return reqif_xml_output
