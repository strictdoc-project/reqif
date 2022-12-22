import html
from typing import List, Optional, Union

from reqif.helpers.lxml import is_self_closed_tag
from reqif.models.reqif_spec_object_type import (
    ReqIFSpecObjectType,
    SpecAttributeDefinition,
    DefaultValueEmptySelfClosedTag,
)
from reqif.models.reqif_types import SpecObjectAttributeType


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
        attribute_definitions: Optional[List[SpecAttributeDefinition]] = None
        xml_spec_attributes = spec_object_type_xml.find("SPEC-ATTRIBUTES")
        if xml_spec_attributes is not None:
            attribute_definitions = []
            for attribute_definition in xml_spec_attributes:
                long_name: Optional[str] = (
                    attribute_definition.attrib["LONG-NAME"]
                    if "LONG-NAME" in attribute_definition.attrib
                    else None
                )

                identifier = attribute_definition.attrib["IDENTIFIER"]
                description: Optional[str] = (
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

                default_value: Union[
                    None, DefaultValueEmptySelfClosedTag, str
                ] = None
                multi_valued: Optional[bool] = None
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

                    xml_default_value = attribute_definition.find(
                        "DEFAULT-VALUE"
                    )
                    if xml_default_value is not None:
                        if is_self_closed_tag(xml_default_value):
                            default_value = DefaultValueEmptySelfClosedTag()
                        else:
                            xml_attribute_value = xml_default_value.find(
                                "ATTRIBUTE-VALUE-STRING"
                            )
                            if xml_attribute_value is not None:
                                default_value = xml_attribute_value.attrib[
                                    "THE-VALUE"
                                ]
                            else:
                                raise NotImplementedError

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

                    xml_default_value = attribute_definition.find(
                        "DEFAULT-VALUE"
                    )
                    if xml_default_value is not None:
                        xml_attribute_value = xml_default_value.find(
                            "ATTRIBUTE-VALUE-INTEGER"
                        )
                        assert xml_attribute_value is not None
                        default_value = xml_attribute_value.attrib["THE-VALUE"]

                elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-REAL":
                    attribute_type = SpecObjectAttributeType.REAL
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-REAL-REF")
                            .text
                        )
                    except Exception as exception:
                        raise NotImplementedError(
                            attribute_definition
                        ) from exception

                    xml_default_value = attribute_definition.find(
                        "DEFAULT-VALUE"
                    )
                    if xml_default_value is not None:
                        xml_attribute_value = xml_default_value.find(
                            "ATTRIBUTE-VALUE-INTEGER"
                        )
                        assert xml_attribute_value is not None
                        default_value = xml_attribute_value.attrib["THE-VALUE"]

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
                    multi_valued_string = (
                        attribute_definition.attrib["MULTI-VALUED"]
                        if "MULTI-VALUED" in attribute_definition.attrib
                        else None
                    )
                    multi_valued = (
                        multi_valued_string == "true"
                        if multi_valued_string
                        else None
                    )
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
                elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-DATE":
                    attribute_type = SpecObjectAttributeType.DATE
                    try:
                        datatype_definition = (
                            attribute_definition.find("TYPE")
                            .find("DATATYPE-DEFINITION-DATE-REF")
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
                    description=description,
                    identifier=identifier,
                    last_change=last_change,
                    datatype_definition=datatype_definition,
                    long_name=long_name,
                    editable=editable,
                    default_value=default_value,
                    multi_valued=multi_valued,
                )
                attribute_definitions.append(attribute_definition)

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

        output += "        " "<SPEC-OBJECT-TYPE"
        if spec_type.description is not None:
            output += f' DESC="{html.escape(spec_type.description)}"'
        output += f' IDENTIFIER="{spec_type.identifier}"'
        if spec_type.last_change is not None:
            output += f' LAST-CHANGE="{spec_type.last_change}"'
        if spec_type.long_name is not None:
            output += f' LONG-NAME="{spec_type.long_name}"'
        output += ">" "\n"

        if spec_type.attribute_definitions is not None:
            output += "          <SPEC-ATTRIBUTES>\n"

            for attribute in spec_type.attribute_definitions:
                output += SpecObjectTypeParser._unparse_attribute_definition(
                    attribute
                )

            output += "          </SPEC-ATTRIBUTES>\n"

        output += "        </SPEC-OBJECT-TYPE>\n"

        return output

    @staticmethod
    def _unparse_attribute_definition(attribute: SpecAttributeDefinition):
        output = ""
        output += (
            "            " "<" f"{attribute.attribute_type.get_spec_type_tag()}"
        )
        if attribute.description:
            output += f' DESC="{attribute.description}"'

        output += f' IDENTIFIER="{attribute.identifier}"'
        if attribute.last_change:
            output += f' LAST-CHANGE="{attribute.last_change}"'
        if attribute.long_name:
            output += f' LONG-NAME="{attribute.long_name}"'
        if attribute.multi_valued is not None:
            multi_valued_value = "true" if attribute.multi_valued else "false"
            output += f' MULTI-VALUED="{multi_valued_value}"'
        if attribute.editable is not None:
            editable_value = "true" if attribute.editable else "false"
            output += f' IS-EDITABLE="{editable_value}"'
        output += ">" "\n"

        children_tags: List[str]
        if attribute.xml_node is not None:
            children_tags = list(
                map(lambda el: el.tag, list(attribute.xml_node))
            )
        else:
            children_tags = ["DEFAULT-VALUE", "TYPE"]
        for tag in children_tags:
            if tag == "DEFAULT-VALUE":
                attribute_default_value = attribute.default_value
                if attribute_default_value is not None:
                    output += (
                        SpecObjectTypeParser._unparse_attribute_default_value(
                            attribute, attribute_default_value
                        )
                    )
            elif tag == "TYPE":
                output += SpecObjectTypeParser._unparse_attribute_type(
                    attribute
                )
            else:
                raise NotImplementedError(tag)

        output += "            </"
        output += f"{attribute.attribute_type.get_spec_type_tag()}"
        output += ">\n"
        return output

    @staticmethod
    def _unparse_attribute_type(
        attribute: SpecAttributeDefinition,
    ):
        output = ""
        output += "              <TYPE>\n"
        output += (
            "                "
            f"<{attribute.attribute_type.get_definition_tag()}>"
            f"{attribute.datatype_definition}"
            f"</{attribute.attribute_type.get_definition_tag()}>"
            "\n"
        )
        output += "              </TYPE>\n"
        return output

    @staticmethod
    def _unparse_attribute_default_value(
        attribute: SpecAttributeDefinition,
        default_value: Union[DefaultValueEmptySelfClosedTag, str],
    ):
        output = ""
        if isinstance(default_value, DefaultValueEmptySelfClosedTag):
            output += "              <DEFAULT-VALUE/>\n"
        else:
            output += (
                "              <DEFAULT-VALUE>\n"
                f"                "
                f"<{attribute.attribute_type.get_attribute_value_tag()}"
                f' THE-VALUE="{attribute.default_value}"/>\n'
                "              </DEFAULT-VALUE>\n"
            )
        return output
