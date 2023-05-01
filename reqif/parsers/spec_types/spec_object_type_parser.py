from typing import Optional

from reqif.helpers.lxml import lxml_escape_for_html
from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
)
from reqif.parsers.attribute_definition_parser import AttributeDefinitionParser


class SpecObjectTypeParser:
    @staticmethod
    def parse(spec_object_type_xml) -> ReqIFSpecObjectType:
        assert (
            spec_object_type_xml.tag == "SPEC-OBJECT-TYPE"
        ), f"{spec_object_type_xml}"

        xml_attributes = spec_object_type_xml.attrib
        spec_description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        try:
            spec_type_id = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None
        spec_last_change = (
            xml_attributes["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attributes
            else None
        )
        spec_type_long_name: Optional[str] = (
            xml_attributes["LONG-NAME"]
            if "LONG-NAME" in xml_attributes
            else None
        )

        attribute_definitions = (
            AttributeDefinitionParser.parse_attribute_definitions(
                spec_object_type_xml
            )
        )

        return ReqIFSpecObjectType(
            description=spec_description,
            identifier=spec_type_id,
            last_change=spec_last_change,
            long_name=spec_type_long_name,
            attribute_definitions=attribute_definitions,
        )

    @staticmethod
    def unparse(spec_type: ReqIFSpecObjectType) -> str:
        output = ""

        output += "        <SPEC-OBJECT-TYPE"
        if spec_type.description is not None:
            output += f' DESC="{lxml_escape_for_html(spec_type.description)}"'
        output += f' IDENTIFIER="{spec_type.identifier}"'
        if spec_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_type.last_change}"'
        if spec_type.long_name is not None:
            escaped_long_name = lxml_escape_for_html(spec_type.long_name)
            output += f' LONG-NAME="{escaped_long_name}"'
        output += ">\n"

        if spec_type.attribute_definitions is not None:
            output += "          <SPEC-ATTRIBUTES>\n"

            output += (
                AttributeDefinitionParser.unparse_xhtml_attribute_definition(
                    attribute_definitions=spec_type.attribute_definitions
                )
            )

            output += "          </SPEC-ATTRIBUTES>\n"

        output += "        </SPEC-OBJECT-TYPE>\n"

        return output
