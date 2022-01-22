from typing import List, Optional

from reqif.models.reqif_spec_object_type import (
    SpecAttributeDefinition,
)
from reqif.models.reqif_specification_type import ReqIFSpecificationType
from reqif.models.reqif_types import SpecObjectAttributeType


class SpecificationTypeParser:
    @staticmethod
    def parse(specification_type_xml) -> ReqIFSpecificationType:
        assert (
            specification_type_xml.tag == "SPECIFICATION-TYPE"
        ), f"{specification_type_xml}"
        attribute_map = {}

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
        try:
            spec_type_long_name = xml_attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError from None

        xml_spec_attributes = specification_type_xml.find("SPEC-ATTRIBUTES")
        attribute_definitions: Optional[List[SpecAttributeDefinition]] = None
        if xml_spec_attributes is not None:
            attribute_definitions = []
            for attribute_definition in xml_spec_attributes:
                long_name = attribute_definition.attrib["LONG-NAME"]
                identifier = attribute_definition.attrib["IDENTIFIER"]
                attribute_description: Optional[str] = (
                    attribute_definition.attrib["DESC"]
                    if "DESC" in attribute_definition.attrib
                    else None
                )
                last_change = (
                    attribute_definition.attrib["LAST-CHANGE"]
                    if "LAST-CHANGE" in attribute_definition.attrib
                    else None
                )
                editable = (
                    attribute_definition.attrib["IS-EDITABLE"]
                    if "IS-EDITABLE" in attribute_definition.attrib
                    else None
                )
                if attribute_definition.tag == "ATTRIBUTE-DEFINITION-STRING":
                    attribute_type = SpecObjectAttributeType.STRING
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-STRING-REF")
                            .text
                        )
                    except Exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from None

                elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-INTEGER":
                    attribute_type = SpecObjectAttributeType.INTEGER
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-INTEGER-REF")
                            .text
                        )
                    except Exception as exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from exception
                elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-BOOLEAN":
                    attribute_type = SpecObjectAttributeType.BOOLEAN
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-BOOLEAN-REF")
                            .text
                        )
                    except Exception as exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from exception

                elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-XHTML":
                    attribute_type = SpecObjectAttributeType.XHTML
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-XHTML-REF")
                            .text
                        )
                    except Exception as exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from exception
                elif (
                    attribute_definition.tag
                    == "ATTRIBUTE-DEFINITION-ENUMERATION"
                ):
                    attribute_type = SpecObjectAttributeType.ENUMERATION
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-ENUMERATION-REF")
                            .text
                        )
                    except Exception as exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from exception
                else:
                    raise NotImplementedError(attribute_definition) from None
                attribute_definition = SpecAttributeDefinition(
                    xml_node=attribute_definition,
                    attribute_type=attribute_type,
                    description=attribute_description,
                    identifier=identifier,
                    last_change=last_change,
                    datatype_definition=datatype_definition,
                    long_name=long_name,
                    editable=editable,
                    default_value=None,
                    multi_valued=None,
                )
                attribute_definitions.append(attribute_definition)
                attribute_map[identifier] = long_name

        return ReqIFSpecificationType(
            description=description,
            identifier=spec_type_id,
            last_change=spec_last_change,
            long_name=spec_type_long_name,
            spec_attributes=attribute_definitions,
            spec_attribute_map=attribute_map,
        )

    @staticmethod
    def unparse(spec_type: ReqIFSpecificationType) -> str:
        output = ""

        output += "        " "<SPECIFICATION-TYPE"
        if spec_type.description is not None:
            output += f' DESC="{spec_type.description}"'
        output += f' IDENTIFIER="{spec_type.identifier}"'
        output += (
            f' LAST-CHANGE="{spec_type.last_change}"'
            f' LONG-NAME="{spec_type.long_name}"'
            f">"
            "\n"
        )

        if spec_type.spec_attributes is not None:
            output += "          <SPEC-ATTRIBUTES>\n"

            for attribute in spec_type.spec_attributes:
                output += (
                    "            "
                    "<"
                    f"{attribute.attribute_type.get_spec_type_tag()}"
                    f' IDENTIFIER="{attribute.identifier}"'
                )
                if attribute.last_change:
                    output += f' LAST-CHANGE="{attribute.last_change}"'
                output += f' LONG-NAME="{attribute.long_name}"'
                if attribute.editable is not None:
                    editable_value = "true" if attribute.editable else "false"
                    output += f' IS-EDITABLE="{editable_value}"'
                output += ">" "\n"
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
