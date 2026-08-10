import logging
from typing import List, Optional

from reqif.models.reqif_relation_group import ReqIFRelationGroup
from reqif.models.reqif_spec_object import SpecObjectAttribute
from reqif.parsers.alternative_id_parser import AlternativeIDParser
from reqif.parsers.attribute_value_parser import AttributeValueParser

logger = logging.getLogger(__name__)


class ReqIFRelationGroupParser:
    @staticmethod
    def parse(xml_relation_group) -> ReqIFRelationGroup:
        assert "RELATION-GROUP" in xml_relation_group.tag, f"{xml_relation_group}"

        attributes = xml_relation_group.attrib
        try:
            identifier = attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError(attributes) from None

        # DESC is optional
        description: Optional[str] = (
            attributes["DESC"] if "DESC" in attributes else None
        )

        # LAST-CHANGE is optional
        last_change: Optional[str] = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )

        # LONG-NAME is optional
        long_name: Optional[str] = (
            attributes["LONG-NAME"] if "LONG-NAME" in attributes else None
        )

        values: Optional[List[SpecObjectAttribute]] = (
            AttributeValueParser.parse_attribute_values(
                xml_relation_group.find("VALUES")
            )
        )

        spec_relations: Optional[List[str]] = None
        xml_spec_relations = xml_relation_group.find("SPEC-RELATIONS")
        if xml_spec_relations is not None:
            spec_relations = []
            for xml_spec_relation_ref in xml_spec_relations:
                spec_relations.append(xml_spec_relation_ref.text)

        type_ref: Optional[str] = None
        xml_type = xml_relation_group.find("TYPE")
        if xml_type is not None:
            xml_type_ref = xml_type.find("RELATION-GROUP-TYPE-REF")
            if xml_type_ref is not None:
                type_ref = xml_type_ref.text

        source_specification_ref: Optional[str] = None
        xml_type = xml_relation_group.find("SOURCE-SPECIFICATION")
        if xml_type is not None:
            xml_type_ref = xml_type.find("SPECIFICATION-REF")
            if xml_type_ref is not None:
                source_specification_ref = xml_type_ref.text

        target_specification_ref: Optional[str] = None
        xml_type = xml_relation_group.find("TARGET-SPECIFICATION")
        if xml_type is not None:
            xml_type_ref = xml_type.find("SPECIFICATION-REF")
            if xml_type_ref is not None:
                target_specification_ref = xml_type_ref.text

        return ReqIFRelationGroup(
            alternative_id=AlternativeIDParser.parse(xml_relation_group),
            identifier=identifier,
            description=description,
            last_change=last_change,
            long_name=long_name,
            type_ref=type_ref,
            source_specification_ref=source_specification_ref,
            target_specification_ref=target_specification_ref,
            spec_relations=spec_relations,
            values=values,
            is_self_closed=False,
        )

    @staticmethod
    def unparse(relation_group: ReqIFRelationGroup) -> str:
        output = ""
        output += "        <RELATION-GROUP"

        if relation_group.description is not None:
            output += f' DESC="{relation_group.description}"'

        output += f' IDENTIFIER="{relation_group.identifier}"'

        if relation_group.last_change is not None:
            output += f' LAST-CHANGE="{relation_group.last_change}"'
        if relation_group.long_name:
            output += f' LONG-NAME="{relation_group.long_name}"'
        output += ">\n"

        output += AlternativeIDParser.unparse(
            relation_group.alternative_id, "          "
        )

        # Emitted first, mirroring SPEC-OBJECT's ["VALUES", "TYPE"] child order.
        # Ordering is not the reason for the position: RELATION-GROUP is an
        # xsd:all, so its children are unordered.
        #
        # The bundled reqif.xsd does not permit VALUES on RELATION-GROUP at all,
        # although the ReqIF spec PDF's MOF model (10.8.33) defines it. That is a
        # known defect of the ReqIF XML schema, called out as such in the prostep
        # ivip ReqIF Implementation Guide v1.8, section 2.11, whose advice is
        # addressed to whoever authors the content.
        #
        # Writing the element is therefore a deliberate deviation from the
        # schema, and whether to ship such a file is the caller's call to make:
        # they know which tools will read the output. So warn rather than refuse,
        # naming the group so the caller can find it. There is no matching
        # warning on the parse side, because sections 2.1, 2.3 and 2.13 of the
        # same guide ask importing tools to be forgiving about what they read and
        # keep the strictness on the export side.
        if relation_group.values is not None and len(relation_group.values) > 0:
            logger.warning(
                "RELATION-GROUP %s: writing a VALUES element, which the ReqIF "
                "XML schema does not permit on RELATION-GROUP (a known schema "
                "defect; see prostep ivip ReqIF Implementation Guide v1.8, "
                "section 2.11). Other ReqIF tools may reject this file or drop "
                "these values silently. Silence this by raising the level of "
                "the %s logger.",
                relation_group.identifier,
                __name__,
            )
        output += AttributeValueParser.unparse_attribute_values(relation_group.values)

        if relation_group.spec_relations is not None:
            output += "          <SPEC-RELATIONS>\n"
            for spec_relation in relation_group.spec_relations:
                output += (
                    f"            <SPEC-RELATION-REF>"
                    f"{spec_relation}"
                    f"</SPEC-RELATION-REF>\n"
                )
            output += "          </SPEC-RELATIONS>\n"

        if relation_group.type_ref is not None:
            output += "          <TYPE>\n"
            output += (
                f"            <RELATION-GROUP-TYPE-REF>"
                f"{relation_group.type_ref}"
                f"</RELATION-GROUP-TYPE-REF>\n"
            )
            output += "          </TYPE>\n"

        if relation_group.source_specification_ref is not None:
            output += "          <SOURCE-SPECIFICATION>\n"
            output += (
                f"            <SPECIFICATION-REF>"
                f"{relation_group.source_specification_ref}"
                f"</SPECIFICATION-REF>\n"
            )
            output += "          </SOURCE-SPECIFICATION>\n"

        if relation_group.target_specification_ref is not None:
            output += "          <TARGET-SPECIFICATION>\n"
            output += (
                f"            <SPECIFICATION-REF>"
                f"{relation_group.target_specification_ref}"
                f"</SPECIFICATION-REF>\n"
            )
            output += "          </TARGET-SPECIFICATION>\n"

        output += "        </RELATION-GROUP>\n"
        return output
