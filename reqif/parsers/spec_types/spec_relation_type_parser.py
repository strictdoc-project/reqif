from typing import Optional

from reqif.models.reqif_spec_relation_type import ReqIFSpecRelationType


class SpecRelationTypeParser:
    @staticmethod
    def parse(xml_spec_relation_type_xml):
        assert (
            xml_spec_relation_type_xml.tag == "SPEC-RELATION-TYPE"
        ), f"{xml_spec_relation_type_xml}"

        xml_attributes = xml_spec_relation_type_xml.attrib
        # Expecting all tools to implement IDENTIFIER and LONG-NAME.
        try:
            identifier = xml_attributes["IDENTIFIER"]
            long_name = xml_attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError(xml_attributes) from None

        # LAST-CHANGE is optional
        # (as per example from SparxSystems Enterprise Architect).
        last_change: Optional[str] = (
            xml_attributes["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attributes
            else None
        )

        return ReqIFSpecRelationType(
            identifier=identifier, last_change=last_change, long_name=long_name
        )

    @staticmethod
    def unparse(spec_relation_type: ReqIFSpecRelationType):
        output = "        <SPEC-RELATION-TYPE "
        output += f'IDENTIFIER="{spec_relation_type.identifier}"'
        if spec_relation_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_relation_type.last_change}"'
        output += f' LONG-NAME="{spec_relation_type.long_name}"/>\n'
        return output
