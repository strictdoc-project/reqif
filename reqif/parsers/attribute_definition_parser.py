from typing import List, Optional, Union

from reqif.helpers.lxml import (
    lxml_escape_for_html,
    lxml_is_self_closed_tag,
    lxml_stringify_namespaced_children,
)
from reqif.models.reqif_spec_object_type import (
    DefaultValueEmptySelfClosedTag,
    SpecAttributeDefinition,
)
from reqif.models.reqif_types import SpecObjectAttributeType


class AttributeDefinitionParser:
    @staticmethod
    def parse_attribute_definitions(
        spec_object_type_xml,
    ) -> Optional[List[SpecAttributeDefinition]]:
        xml_spec_attributes = spec_object_type_xml.find("SPEC-ATTRIBUTES")
        if xml_spec_attributes is None:
            return None

        attribute_definitions: List[SpecAttributeDefinition] = []
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

            default_value_definition_ref: Optional[str] = None
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
                    raise NotImplementedError(attribute_definition) from None

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
                if xml_default_value is not None:
                    if lxml_is_self_closed_tag(xml_default_value):
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

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
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

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
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

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
                if xml_default_value is not None:
                    xml_attribute_value = xml_default_value.find(
                        "ATTRIBUTE-VALUE-BOOLEAN"
                    )
                    assert xml_attribute_value is not None
                    default_value = xml_attribute_value.attrib["THE-VALUE"]

                    xml_definition = xml_attribute_value.find("DEFINITION")
                    if xml_definition is not None:
                        xml_attribute_definition = xml_definition.find(
                            "ATTRIBUTE-DEFINITION-BOOLEAN-REF"
                        )
                        if xml_attribute_definition is not None:
                            default_value_definition_ref = (
                                xml_attribute_definition.text
                            )
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

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
                if xml_default_value is None:
                    pass
                elif lxml_is_self_closed_tag(xml_default_value):
                    default_value = DefaultValueEmptySelfClosedTag()
                else:
                    xml_attribute_value = xml_default_value.find(
                        "ATTRIBUTE-VALUE-XHTML"
                    )
                    if xml_attribute_value is not None:
                        xml_definition_value = xml_attribute_value.find(
                            "DEFINITION"
                        )
                        if xml_definition_value is not None:
                            xml_attribute_ref = xml_definition_value.find(
                                "ATTRIBUTE-DEFINITION-XHTML-REF"
                            )
                            assert xml_attribute_ref is not None
                            default_value_definition_ref = (
                                xml_attribute_ref.text
                            )
                        xml_values = xml_attribute_value.find("THE-VALUE")
                        default_value = lxml_stringify_namespaced_children(
                            xml_values
                        )
                    else:
                        raise NotImplementedError
            elif attribute_definition.tag == "ATTRIBUTE-DEFINITION-ENUMERATION":
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

                xml_default_value = attribute_definition.find("DEFAULT-VALUE")
                if xml_default_value is not None:
                    if lxml_is_self_closed_tag(xml_default_value):
                        default_value = DefaultValueEmptySelfClosedTag()
                    else:
                        xml_attribute_value = xml_default_value.find(
                            "ATTRIBUTE-VALUE-ENUMERATION"
                        )
                        if xml_attribute_value is not None:
                            xml_definition_value = xml_attribute_value.find(
                                "DEFINITION"
                            )
                            if xml_definition_value is not None:
                                xml_attribute_ref = (
                                    xml_definition_value.find(  # noqa: E501
                                        "ATTRIBUTE-DEFINITION-ENUMERATION-REF"
                                    )
                                )
                                default_value_definition_ref = (
                                    xml_attribute_ref.text
                                )
                            xml_values = xml_attribute_value.find("VALUES")
                            if xml_values is not None:
                                xml_enum_value_ref = xml_values.find(
                                    "ENUM-VALUE-REF"
                                )
                                default_value = xml_enum_value_ref.text
                        else:
                            raise NotImplementedError
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
                default_value_definition_ref=default_value_definition_ref,
                default_value=default_value,
                multi_valued=multi_valued,
            )
            attribute_definitions.append(attribute_definition)

        return attribute_definitions

    @staticmethod
    def parse_xhtml_attribute_definition(
        xml_attribute_definition,
    ) -> SpecAttributeDefinition:
        assert xml_attribute_definition.tag == "ATTRIBUTE-DEFINITION-XHTML"

        long_name: Optional[str] = (
            xml_attribute_definition.attrib["LONG-NAME"]
            if "LONG-NAME" in xml_attribute_definition.attrib
            else None
        )

        identifier = xml_attribute_definition.attrib["IDENTIFIER"]
        description: Optional[str] = (
            xml_attribute_definition.attrib["DESC"]
            if "DESC" in xml_attribute_definition.attrib
            else None
        )
        last_change = (
            xml_attribute_definition.attrib["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attribute_definition.attrib
            else None
        )
        editable = (
            xml_attribute_definition.attrib["IS-EDITABLE"]
            if "IS-EDITABLE" in xml_attribute_definition.attrib
            else None
        )

        default_value_definition_ref: Optional[str] = None
        default_value: Union[None, DefaultValueEmptySelfClosedTag, str] = None

        try:
            datatype_definition = (
                xml_attribute_definition.find("TYPE")
                .find("DATATYPE-DEFINITION-XHTML-REF")
                .text
            )
        except Exception as exception:
            raise NotImplementedError(xml_attribute_definition) from exception

        xml_default_value = xml_attribute_definition.find("DEFAULT-VALUE")
        if xml_default_value is None:
            pass
        elif lxml_is_self_closed_tag(xml_default_value):
            default_value = DefaultValueEmptySelfClosedTag()
        else:
            xml_attribute_value = xml_default_value.find(
                "ATTRIBUTE-VALUE-XHTML"
            )
            if xml_attribute_value is not None:
                xml_definition_value = xml_attribute_value.find("DEFINITION")
                if xml_definition_value is not None:
                    xml_attribute_ref = xml_definition_value.find(
                        "ATTRIBUTE-DEFINITION-XHTML-REF"
                    )
                    assert xml_attribute_ref is not None
                    default_value_definition_ref = xml_attribute_ref.text
                xml_values = xml_attribute_value.find("THE-VALUE")
                default_value = lxml_stringify_namespaced_children(xml_values)
            else:
                raise NotImplementedError

        return SpecAttributeDefinition(
            xml_node=xml_attribute_definition,
            attribute_type=SpecObjectAttributeType.XHTML,
            description=description,
            identifier=identifier,
            last_change=last_change,
            datatype_definition=datatype_definition,
            long_name=long_name,
            editable=editable,
            default_value_definition_ref=default_value_definition_ref,
            default_value=default_value,
            multi_valued=False,
        )

    @staticmethod
    def unparse_xhtml_attribute_definition(
        attribute_definitions: List[SpecAttributeDefinition],
    ) -> str:
        output = ""
        for attribute in attribute_definitions:
            output += AttributeDefinitionParser._unparse_attribute_definition(
                attribute
            )
        return output

    @staticmethod
    def _unparse_attribute_definition(attribute: SpecAttributeDefinition):
        output = ""
        output += f"            <{attribute.attribute_type.get_spec_type_tag()}"
        if attribute.description is not None:
            output += f' DESC="{lxml_escape_for_html(attribute.description)}"'
        output += f' IDENTIFIER="{attribute.identifier}"'
        if attribute.editable is not None:
            editable_value = "true" if attribute.editable else "false"
            output += f' IS-EDITABLE="{editable_value}"'
        if attribute.last_change:
            output += f' LAST-CHANGE="{attribute.last_change}"'
        if attribute.long_name is not None:
            escaped_long_name = lxml_escape_for_html(attribute.long_name)
            output += f' LONG-NAME="{escaped_long_name}"'
        if attribute.multi_valued is not None:
            multi_valued_value = "true" if attribute.multi_valued else "false"
            output += f' MULTI-VALUED="{multi_valued_value}"'
        output += ">\n"

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
                    unparsed_default_value = AttributeDefinitionParser._unparse_attribute_default_value(  # noqa: E501
                        attribute, attribute_default_value
                    )
                    output += unparsed_default_value
            elif tag == "TYPE":
                output += AttributeDefinitionParser._unparse_attribute_type(
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
            return output
        if attribute.attribute_type == SpecObjectAttributeType.ENUMERATION:
            assert attribute.default_value_definition_ref is not None, attribute
            output += (
                "              <DEFAULT-VALUE>\n"
                f"                "
                f"<{attribute.attribute_type.get_attribute_value_tag()}>\n"
                f"                  <DEFINITION>\n"
                f"                    <ATTRIBUTE-DEFINITION-ENUMERATION-REF>"
                f"{attribute.default_value_definition_ref}"
                f"</ATTRIBUTE-DEFINITION-ENUMERATION-REF>\n"
                f"                  </DEFINITION>\n"
                f"                  <VALUES>\n"
                f"                    <ENUM-VALUE-REF>"
                f"{attribute.default_value}</ENUM-VALUE-REF>\n"
                f"                  </VALUES>\n"
                f"                "
                f"</{attribute.attribute_type.get_attribute_value_tag()}>\n"
                "              </DEFAULT-VALUE>\n"
            )
        elif attribute.attribute_type == SpecObjectAttributeType.XHTML:
            assert attribute.default_value_definition_ref is not None, attribute
            output += (
                "              <DEFAULT-VALUE>\n"
                "                <ATTRIBUTE-VALUE-XHTML>\n"
                "                  <DEFINITION>\n"
                "                    <ATTRIBUTE-DEFINITION-XHTML-REF>"
                f"{attribute.default_value_definition_ref}"
                f"</ATTRIBUTE-DEFINITION-XHTML-REF>\n"
                "                  </DEFINITION>\n"
                "                  <THE-VALUE>"
                f"{attribute.default_value}</THE-VALUE>\n"
                "                </ATTRIBUTE-VALUE-XHTML>\n"
                "              </DEFAULT-VALUE>\n"
            )
        elif attribute.attribute_type == SpecObjectAttributeType.BOOLEAN:
            assert attribute.default_value_definition_ref is not None, attribute
            output += (
                "              <DEFAULT-VALUE>\n"
                f"                <ATTRIBUTE-VALUE-BOOLEAN "
                f'THE-VALUE="{attribute.default_value}">\n'
                "                  <DEFINITION>\n"
                "                    <ATTRIBUTE-DEFINITION-BOOLEAN-REF>"
                f"{attribute.default_value_definition_ref}"
                f"</ATTRIBUTE-DEFINITION-BOOLEAN-REF>\n"
                "                  </DEFINITION>\n"
                "                </ATTRIBUTE-VALUE-BOOLEAN>\n"
                "              </DEFAULT-VALUE>\n"
            )
        else:
            output += (
                "              <DEFAULT-VALUE>\n"
                f"                "
                f"<{attribute.attribute_type.get_attribute_value_tag()}"
                f' THE-VALUE="{attribute.default_value}"/>\n'
                "              </DEFAULT-VALUE>\n"
            )
        return output
