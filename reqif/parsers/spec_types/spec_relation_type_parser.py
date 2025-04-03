import html
from typing import Optional

from reqif.helpers.lxml import lxml_is_self_closed_tag
from reqif.models.reqif_spec_relation_type import ReqIFSpecRelationType
from reqif.parsers.attribute_definition_parser import AttributeDefinitionParser


class SpecRelationTypeParser:
    @staticmethod
    def parse(xml_spec_relation_type_xml) -> ReqIFSpecRelationType:
        assert xml_spec_relation_type_xml.tag == "SPEC-RELATION-TYPE", (
            f"{xml_spec_relation_type_xml}"
        )
        is_self_closed = lxml_is_self_closed_tag(xml_spec_relation_type_xml)

        xml_attributes = xml_spec_relation_type_xml.attrib
        # Expecting all tools to implement IDENTIFIER and LONG-NAME.
        try:
            identifier = xml_attributes["IDENTIFIER"]
            long_name = xml_attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError(xml_attributes) from None

        description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        last_change: Optional[str] = (
            xml_attributes["LAST-CHANGE"] if "LAST-CHANGE" in xml_attributes else None
        )

        attribute_definitions = AttributeDefinitionParser.parse_attribute_definitions(
            xml_spec_relation_type_xml
        )

        return ReqIFSpecRelationType(
            is_self_closed=is_self_closed,
            description=description,
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
            attribute_definitions=attribute_definitions,
        )

    @staticmethod
    def unparse(spec_relation_type: ReqIFSpecRelationType):
        output = "        <SPEC-RELATION-TYPE"
        if spec_relation_type.description is not None:
            output += f' DESC="{html.escape(spec_relation_type.description)}"'
        output += f' IDENTIFIER="{spec_relation_type.identifier}"'
        if spec_relation_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_relation_type.last_change}"'
        if spec_relation_type.long_name is not None:
            output += f' LONG-NAME="{spec_relation_type.long_name}"'
        if spec_relation_type.is_self_closed:
            output += "/>\n"
            return output

        output += ">\n"

        if spec_relation_type.attribute_definitions is not None:
            output += "          <SPEC-ATTRIBUTES>\n"

            output += AttributeDefinitionParser.unparse_xhtml_attribute_definition(  # noqa: E501
                attribute_definitions=spec_relation_type.attribute_definitions
            )

            output += "          </SPEC-ATTRIBUTES>\n"

        output += "        </SPEC-RELATION-TYPE>\n"

        return output
