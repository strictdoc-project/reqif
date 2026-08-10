import html
from typing import List, Optional

from reqif.models.error_handling import ReqIFMissingTagException
from reqif.models.reqif_spec_object import SpecObjectAttribute
from reqif.models.reqif_spec_relation import (
    ReqIFSpecRelation,
)
from reqif.parsers.alternative_id_parser import AlternativeIDParser
from reqif.parsers.attribute_value_parser import AttributeValueParser


class SpecRelationParser:
    @staticmethod
    def parse(xml_spec_relation) -> ReqIFSpecRelation:
        assert xml_spec_relation.tag == "SPEC-RELATION"

        children_tags = list(map(lambda el: el.tag, list(xml_spec_relation)))
        assert "TYPE" in children_tags
        if "SOURCE" not in children_tags:
            raise ReqIFMissingTagException(
                xml_node=xml_spec_relation, tag="SOURCE"
            ) from None
        if "TARGET" not in children_tags:
            raise ReqIFMissingTagException(
                xml_node=xml_spec_relation, tag="TARGET"
            ) from None

        attributes = xml_spec_relation.attrib
        assert "IDENTIFIER" in attributes, f"{attributes}"
        identifier = attributes["IDENTIFIER"]

        description: Optional[str] = (
            attributes["DESC"] if "DESC" in attributes else None
        )

        last_change: Optional[str] = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )

        long_name: Optional[str] = (
            attributes["LONG-NAME"] if "LONG-NAME" in attributes else None
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

        # Delegate to the shared helper rather than hand-rolling the loop: it
        # keeps every value instead of only the first, and it covers all seven
        # ATTRIBUTE-VALUE-* kinds rather than STRING/INTEGER/XHTML alone.
        xml_values = xml_spec_relation.find("VALUES")
        values: Optional[List[SpecObjectAttribute]] = (
            AttributeValueParser.parse_attribute_values(xml_values)
        )

        spec_relation = ReqIFSpecRelation(
            alternative_id=AlternativeIDParser.parse(xml_spec_relation),
            xml_node=xml_spec_relation,
            description=description,
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
            relation_type_ref=relation_type_ref,
            source=spec_relation_source,
            target=spec_relation_target,
            values=values,
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
        if spec_relation.long_name is not None:
            output += f' LONG-NAME="{html.escape(spec_relation.long_name)}"'
        output += ">\n"

        children_tags: List[str]
        if spec_relation.xml_node is not None:
            children_tags = list(map(lambda el: el.tag, list(spec_relation.xml_node)))
        else:
            children_tags = ["ALTERNATIVE-ID", "TYPE", "SOURCE", "TARGET", "VALUES"]
        for tag in children_tags:
            if tag == "ALTERNATIVE-ID":
                output += AlternativeIDParser.unparse(
                    spec_relation.alternative_id, "          "
                )
            elif tag == "TYPE":
                output += SpecRelationParser._unparse_spec_relation_type(spec_relation)
            elif tag == "SOURCE":
                output += SpecRelationParser._unparse_spec_relation_source(
                    spec_relation
                )
            elif tag == "TARGET":
                output += SpecRelationParser._unparse_spec_relation_target(
                    spec_relation
                )
            elif tag == "VALUES":
                output += AttributeValueParser.unparse_attribute_values(
                    spec_relation.values
                )
            else:
                raise NotImplementedError(tag)

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
    def _unparse_spec_relation_source(
        spec_relation: ReqIFSpecRelation,
    ) -> str:
        output = ""
        output += "          <SOURCE>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.source}</SPEC-OBJECT-REF>\n"
        output += "          </SOURCE>\n"
        return output

    @staticmethod
    def _unparse_spec_relation_target(
        spec_relation: ReqIFSpecRelation,
    ) -> str:
        output = ""
        output += "          <TARGET>\n"
        output += "            "
        output += f"<SPEC-OBJECT-REF>{spec_relation.target}</SPEC-OBJECT-REF>\n"
        output += "          </TARGET>\n"
        return output
