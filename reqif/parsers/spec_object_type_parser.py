from typing import List

from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
    SpecAttributeDefinition,
)
from reqif.models.reqif_types import SpecObjectAttributeType


class SpecObjectTypeParser:
    @staticmethod
    def parse(spec_object_type_xml) -> ReqIFSpecObjectType:
        assert (
            spec_object_type_xml.tag == "SPEC-OBJECT-TYPE"
        ), f"{spec_object_type_xml}"
        attribute_map = {}

        xml_attributes = spec_object_type_xml.attrib
        try:
            spec_type_id = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None

        try:
            spec_type_long_name = xml_attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError from None

        spec_attributes = list(spec_object_type_xml)[0]
        attribute_definitions: List[SpecAttributeDefinition] = []
        for attribute_definition in spec_attributes:
            try:
                long_name = attribute_definition.attrib["LONG-NAME"]
                identifier = attribute_definition.attrib["IDENTIFIER"]
                last_change = attribute_definition.attrib["LAST-CHANGE"]
                datatype_definition = (
                    attribute_definition.find("TYPE")
                    .find("DATATYPE-DEFINITION-STRING-REF")
                    .text
                )
            except Exception:
                raise NotImplementedError(attribute_definition) from None
            if attribute_definition.tag == "ATTRIBUTE-DEFINITION-STRING":
                attribute_definition = SpecAttributeDefinition(
                    attribute_type=SpecObjectAttributeType.STRING,
                    identifier=identifier,
                    last_change=last_change,
                    datatype_definition=datatype_definition,
                    long_name=long_name,
                )
            else:
                raise NotImplementedError
            attribute_definitions.append(attribute_definition)
            attribute_map[identifier] = long_name

        return ReqIFSpecObjectType(
            spec_type_id,
            spec_type_long_name,
            attribute_definitions,
            attribute_map,
        )

    @staticmethod
    def unparse(spec_type: ReqIFSpecObjectType) -> str:
        output = ""

        output += (
            "        "
            "<SPEC-OBJECT-TYPE "
            f'IDENTIFIER="{spec_type.identifier}" '
            'LAST-CHANGE="2021-10-15T08:59:33.583+02:00" '
            f'LONG-NAME="{spec_type.long_name}">'
            "\n"
        )

        output += "          <SPEC-ATTRIBUTES>\n"

        for attribute in spec_type.attribute_definitions:
            if attribute.attribute_type == SpecObjectAttributeType.STRING:

                output += (
                    "            "
                    "<ATTRIBUTE-DEFINITION-STRING "
                    f'IDENTIFIER="{attribute.identifier}" '
                    f'LAST-CHANGE="{attribute.last_change}" '
                    f'LONG-NAME="{attribute.long_name}">'
                    "\n"
                )
                output += "              <TYPE>\n"

                output += (
                    "                "
                    "<DATATYPE-DEFINITION-STRING-REF>"
                    f"{attribute.datatype_definition}"
                    "</DATATYPE-DEFINITION-STRING-REF>"
                    "\n"
                )

                output += "              </TYPE>\n"

                output += "            </ATTRIBUTE-DEFINITION-STRING>\n"
            else:
                raise NotImplementedError

        output += "          </SPEC-ATTRIBUTES>\n"

        output += "        </SPEC-OBJECT-TYPE>\n"

        return output
