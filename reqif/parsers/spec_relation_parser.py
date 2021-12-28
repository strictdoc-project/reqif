from typing import Optional

from reqif.models.reqif_spec_relation import (
    ReqIFSpecRelation,
)


class SpecRelationParser:
    @staticmethod
    def parse(xml_spec_relation) -> ReqIFSpecRelation:
        assert xml_spec_relation.tag == "SPEC-RELATION"

        children_tags = list(map(lambda el: el.tag, list(xml_spec_relation)))
        type_then_source_order = True
        if "TYPE" in children_tags and "SOURCE" in children_tags:
            type_then_source_order = children_tags.index(
                "TYPE"
            ) < children_tags.index("SOURCE")

        attributes = xml_spec_relation.attrib
        assert "IDENTIFIER" in attributes, f"{attributes}"
        identifier = attributes["IDENTIFIER"]

        description: Optional[str] = (
            attributes["DESC"] if "DESC" in attributes else None
        )

        last_change: Optional[str] = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )

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
            type_then_source_order=type_then_source_order,
            description=description,
            identifier=identifier,
            last_change=last_change,
            relation_type_ref=relation_type_ref,
            source=spec_relation_source,
            target=spec_relation_target,
        )
        return spec_relation

    @staticmethod
    def unparse(spec_relation: ReqIFSpecRelation):
        output = "        <SPEC-RELATION"
        if spec_relation.description is not None:
            output += f' DESC="{spec_relation.description}"'
        output += f' IDENTIFIER="{spec_relation.identifier}"'
        if spec_relation.last_change is not None:
            output += f' LAST-CHANGE="{spec_relation.last_change}"'
        output += ">\n"

        if spec_relation.type_then_source_order:
            output += SpecRelationParser._unparse_spec_relation_type(
                spec_relation
            )
            output += (
                SpecRelationParser._unparse_spec_relation_source_and_target(
                    spec_relation
                )
            )
        else:
            output += (
                SpecRelationParser._unparse_spec_relation_source_and_target(
                    spec_relation
                )
            )
            output += SpecRelationParser._unparse_spec_relation_type(
                spec_relation
            )

        output += "        </SPEC-RELATION>\n"
        return output

    @staticmethod
    def _unparse_spec_relation_type(spec_relation: ReqIFSpecRelation) -> str:
        output = ""
        output += "          <TYPE>\n"
        output += "            "
        output += (
            "<SPEC-RELATION-TYPE-REF>"
            f"{spec_relation.relation_type_ref}"
            "</SPEC-RELATION-TYPE-REF>\n"
        )
        output += "          </TYPE>\n"
        return output

    @staticmethod
    def _unparse_spec_relation_source_and_target(
        spec_relation: ReqIFSpecRelation,
    ) -> str:
        output = ""
        output += "          <SOURCE>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.source}</SPEC-OBJECT-REF>\n"
        output += "          </SOURCE>\n"
        output += "          <TARGET>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.target}</SPEC-OBJECT-REF>\n"
        output += "          </TARGET>\n"
        return output
