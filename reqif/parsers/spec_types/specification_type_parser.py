from typing import Dict, Optional

from reqif.helpers.lxml import lxml_is_self_closed_tag
from reqif.models.reqif_specification_type import ReqIFSpecificationType
from reqif.parsers.attribute_definition_parser import AttributeDefinitionParser


class SpecificationTypeParser:
    @staticmethod
    def parse(specification_type_xml) -> ReqIFSpecificationType:
        assert (
            specification_type_xml.tag == "SPECIFICATION-TYPE"
        ), f"{specification_type_xml}"
        is_self_closed = lxml_is_self_closed_tag(specification_type_xml)

        attribute_map: Dict[str, str] = {}

        xml_attributes = specification_type_xml.attrib
        description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        try:
            spec_type_id = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None
        try:
            spec_last_change = xml_attributes["LAST-CHANGE"]
        except Exception:
            raise NotImplementedError from None

        spec_type_long_name = (
            xml_attributes["LONG-NAME"]
            if "LONG-NAME" in xml_attributes
            else None
        )

        attribute_definitions = (
            AttributeDefinitionParser.parse_attribute_definitions(
                specification_type_xml
            )
        )
        # FIXME: Double-check if this is really needed.
        if attribute_definitions is not None:
            for attribute_definition in attribute_definitions:
                assert attribute_definition.long_name is not None
                attribute_map[
                    attribute_definition.identifier
                ] = attribute_definition.long_name

        return ReqIFSpecificationType(
            description=description,
            identifier=spec_type_id,
            last_change=spec_last_change,
            long_name=spec_type_long_name,
            spec_attributes=attribute_definitions,
            spec_attribute_map=attribute_map,
            is_self_closed=is_self_closed,
        )

    @staticmethod
    def unparse(spec_type: ReqIFSpecificationType) -> str:
        output = ""

        output += "        <SPECIFICATION-TYPE"
        if spec_type.description is not None:
            output += f' DESC="{spec_type.description}"'
        output += f' IDENTIFIER="{spec_type.identifier}"'
        if spec_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_type.last_change}"'
        if spec_type.long_name is not None:
            output += f' LONG-NAME="{spec_type.long_name}"'

        # Some documents have a SPECIFICATION-TYPE without any SPEC-ATTRIBUTES.
        if spec_type.is_self_closed:
            output += "/>\n"
            return output
        else:
            output += ">\n"

        if spec_type.spec_attributes is not None:
            output += "          <SPEC-ATTRIBUTES>\n"

            for attribute in spec_type.spec_attributes:
                output += (
                    "            "
                    "<"
                    f"{attribute.attribute_type.get_spec_type_tag()}"
                )
                if attribute.description is not None:
                    output += f' DESC="{attribute.description}"'
                output += f' IDENTIFIER="{attribute.identifier}"'
                if attribute.editable is not None:
                    editable_value = "true" if attribute.editable else "false"
                    output += f' IS-EDITABLE="{editable_value}"'
                if attribute.last_change:
                    output += f' LAST-CHANGE="{attribute.last_change}"'
                output += f' LONG-NAME="{attribute.long_name}"'
                output += ">\n"
                output += "              <TYPE>\n"
                output += (
                    "                "
                    f"<{attribute.attribute_type.get_definition_tag()}>"
                    f"{attribute.datatype_definition}"
                    f"</{attribute.attribute_type.get_definition_tag()}>"
                    "\n"
                )
                output += "              </TYPE>\n"
                output += "            </"
                output += f"{attribute.attribute_type.get_spec_type_tag()}"
                output += ">\n"

            output += "          </SPEC-ATTRIBUTES>\n"

        output += "        </SPECIFICATION-TYPE>\n"

        return output
