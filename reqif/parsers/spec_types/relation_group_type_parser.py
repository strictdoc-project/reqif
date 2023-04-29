import html
from typing import Optional

from reqif.helpers.lxml import lxml_is_self_closed_tag
from reqif.models.reqif_relation_group_type import ReqIFRelationGroupType


class RelationGroupTypeParser:
    @staticmethod
    def parse(xml_spec_relation_type_xml) -> ReqIFRelationGroupType:
        assert (
            xml_spec_relation_type_xml.tag == "RELATION-GROUP-TYPE"
        ), f"{xml_spec_relation_type_xml}"
        is_self_closed = lxml_is_self_closed_tag(xml_spec_relation_type_xml)

        xml_attributes = xml_spec_relation_type_xml.attrib
        # Expecting all tools to implement IDENTIFIER and LONG-NAME.
        try:
            identifier = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError(xml_attributes) from None

        long_name: Optional[str] = (
            xml_attributes["LONG-NAME"]
            if "LONG-NAME" in xml_attributes
            else None
        )

        description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        last_change: Optional[str] = (
            xml_attributes["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attributes
            else None
        )

        return ReqIFRelationGroupType(
            is_self_closed=is_self_closed,
            description=description,
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
        )

    @staticmethod
    def unparse(spec_relation_type: ReqIFRelationGroupType):
        output = "        <RELATION-GROUP-TYPE"
        if spec_relation_type.description is not None:
            output += f' DESC="{html.escape(spec_relation_type.description)}"'
        output += f' IDENTIFIER="{spec_relation_type.identifier}"'
        if spec_relation_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_relation_type.last_change}"'
        if spec_relation_type.long_name is not None:
            output += f' LONG-NAME="{spec_relation_type.long_name}"'
        if spec_relation_type.is_self_closed:
            output += "/>\n"
        else:
            output += ">\n"
            output += "        </SPEC-RELATION-TYPE>\n"
        return output
