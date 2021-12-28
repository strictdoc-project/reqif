from reqif.models.reqif_spec_relation import (
    ReqIFSpecRelation,
)


class SpecRelationParser:
    @staticmethod
    def parse(xml_spec_relation) -> ReqIFSpecRelation:
        assert xml_spec_relation.tag == "SPEC-RELATION"
        attributes = xml_spec_relation.attrib

        assert "IDENTIFIER" in attributes, f"{attributes}"
        identifier = attributes["IDENTIFIER"]

        relation_type_ref = (
            xml_spec_relation.find("TYPE").find("SPEC-RELATION-TYPE-REF").text
        )
        spec_relation_source = (
            xml_spec_relation.find("SOURCE").find("SPEC-OBJECT-REF").text
        )
        spec_relation_target = (
            xml_spec_relation.find("TARGET").find("SPEC-OBJECT-REF").text
        )

        spec_relation = ReqIFSpecRelation(
            identifier=identifier,
            relation_type_ref=relation_type_ref,
            source=spec_relation_source,
            target=spec_relation_target,
        )
        return spec_relation

    @staticmethod
    def unparse(spec_relation: ReqIFSpecRelation):
        output = (
            f'        <SPEC-RELATION IDENTIFIER="{spec_relation.identifier}">\n'
        )
        output += "          <TYPE>\n"
        output += "            "
        output += (
            "<SPEC-RELATION-TYPE-REF>"
            f"{spec_relation.relation_type_ref}"
            "</SPEC-RELATION-TYPE-REF>\n"
        )
        output += "          </TYPE>\n"
        output += "          <SOURCE>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.source}</SPEC-OBJECT-REF>\n"
        output += "          </SOURCE>\n"
        output += "          <TARGET>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.target}</SPEC-OBJECT-REF>\n"
        output += "          </TARGET>\n"
        output += "        </SPEC-RELATION>\n"
        return output
