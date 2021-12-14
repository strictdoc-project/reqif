from reqif.models.reqif_spec_relation_type import ReqIFSpecRelationType


class SpecRelationTypeParser:
    @staticmethod
    def parse(xml_spec_relation_type_xml):
        assert (
            xml_spec_relation_type_xml.tag == "SPEC-RELATION-TYPE"
        ), f"{xml_spec_relation_type_xml}"

        xml_attributes = xml_spec_relation_type_xml.attrib
        try:
            identifier = xml_attributes["IDENTIFIER"]
            last_change = xml_attributes["LAST-CHANGE"]
            long_name = xml_attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError from None

        return ReqIFSpecRelationType(
            identifier=identifier, last_change=last_change, long_name=long_name
        )

    @staticmethod
    def unparse(spec_relation_type: ReqIFSpecRelationType):
        return (
            "        "
            "<SPEC-RELATION-TYPE "
            f'IDENTIFIER="{spec_relation_type.identifier}" '
            f'LAST-CHANGE="{spec_relation_type.last_change}" '
            f'LONG-NAME="{spec_relation_type.long_name}"/>\n'
        )
