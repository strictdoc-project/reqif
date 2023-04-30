from typing import List, Optional

from reqif.models.reqif_relation_group import ReqIFRelationGroup


class ReqIFRelationGroupParser:
    @staticmethod
    def parse(xml_relation_group) -> ReqIFRelationGroup:
        assert (
            "RELATION-GROUP" in xml_relation_group.tag
        ), f"{xml_relation_group}"

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
            identifier=identifier,
            description=description,
            last_change=last_change,
            long_name=long_name,
            type_ref=type_ref,
            source_specification_ref=source_specification_ref,
            target_specification_ref=target_specification_ref,
            spec_relations=spec_relations,
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
