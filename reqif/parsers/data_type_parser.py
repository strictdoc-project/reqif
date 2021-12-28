from typing import Union

from lxml import etree

from reqif.models.reqif_data_type import (
    ReqIFDataTypeDefinitionString,
    ReqIFDataTypeDefinitionEnumeration,
    ReqIFDataTypeDefinitionInteger,
)


class DataTypeParser:
    @staticmethod
    def parse(
        data_type_xml,
    ) -> Union[
        ReqIFDataTypeDefinitionString,
        ReqIFDataTypeDefinitionInteger,
        ReqIFDataTypeDefinitionEnumeration,
    ]:
        assert "DATATYPE-DEFINITION-" in data_type_xml.tag
        attributes = data_type_xml.attrib
        identifier = attributes["IDENTIFIER"]
        last_change = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )
        long_name = attributes["LONG-NAME"]
        description = attributes["DESC"] if "DESC" in attributes else None
        values_map = {}

        if data_type_xml.tag == "DATATYPE-DEFINITION-ENUMERATION":
            specified_values = data_type_xml.find("SPECIFIED-VALUES")

            for specified_value in specified_values:
                specified_value_attributes = specified_value.attrib
                specified_value_identifier = specified_value_attributes[
                    "IDENTIFIER"
                ]

                properties = specified_value.find("PROPERTIES")

                embedded_value = properties.find("EMBEDDED-VALUE")
                embedded_value_attributes = embedded_value.attrib
                embedded_value_key = embedded_value_attributes["KEY"]

                values_map[specified_value_identifier] = embedded_value_key
            return ReqIFDataTypeDefinitionEnumeration(identifier, values_map)

        if data_type_xml.tag == "DATATYPE-DEFINITION-STRING":
            max_length = (
                attributes["MAX-LENGTH"] if "MAX-LENGTH" in attributes else None
            )

            return ReqIFDataTypeDefinitionString(
                description=description,
                identifier=identifier,
                last_change=last_change,
                long_name=long_name,
                max_length=max_length,
            )

        if data_type_xml.tag == "DATATYPE-DEFINITION-INTEGER":
            return ReqIFDataTypeDefinitionInteger(
                description=description,
                identifier=identifier,
                last_change=last_change,
                long_name=long_name,
            )

        # TODO: All the following is parsed to just String.
        if data_type_xml.tag == "DATATYPE-DEFINITION-XHTML":
            return ReqIFDataTypeDefinitionString(
                description=description,
                identifier=identifier,
                last_change=last_change,
                long_name=long_name,
                max_length=None,
            )

        if data_type_xml.tag == "DATATYPE-DEFINITION-BOOLEAN":
            return ReqIFDataTypeDefinitionString(
                description=description,
                identifier=identifier,
                last_change=last_change,
                long_name=long_name,
                max_length=None,
            )

        raise NotImplementedError(etree.tostring(data_type_xml))

    @staticmethod
    def unparse(
        data_type_definition: Union[
            ReqIFDataTypeDefinitionString, ReqIFDataTypeDefinitionEnumeration
        ]
    ) -> str:
        if isinstance(data_type_definition, ReqIFDataTypeDefinitionString):
            output = "        <DATATYPE-DEFINITION-STRING"
            if data_type_definition.description:
                output += f' DESC="{data_type_definition.description}"'

            output += f' IDENTIFIER="{data_type_definition.identifier}"'
            if data_type_definition.last_change:
                output += f' LAST-CHANGE="{data_type_definition.last_change}"'
            output += f' LONG-NAME="{data_type_definition.long_name}"'
            if data_type_definition.max_length:
                output += f' MAX-LENGTH="{data_type_definition.max_length}"'
            output += "/>\n"
            return output
        if isinstance(data_type_definition, ReqIFDataTypeDefinitionInteger):
            output = "        <DATATYPE-DEFINITION-INTEGER"
            if data_type_definition.description:
                output += f' DESC="{data_type_definition.description}"'

            output += f' IDENTIFIER="{data_type_definition.identifier}"'
            if data_type_definition.last_change:
                output += f' LAST-CHANGE="{data_type_definition.last_change}"'
            output += f' LONG-NAME="{data_type_definition.long_name}"'
            output += "/>\n"
            return output
        raise NotImplementedError
