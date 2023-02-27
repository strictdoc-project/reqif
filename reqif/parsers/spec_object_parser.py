import html
from typing import List, Optional

from lxml import etree

from reqif.helpers.lxml import (
    lxml_convert_children_from_reqif_ns_xhtml_string,
    lxml_stringify_children,
    lxml_stringify_namespaced_children,
)
from reqif.helpers.string.xhtml_indent import reqif_unindent_xhtml_string
from reqif.models.reqif_spec_object import (
    ReqIFSpecObject,
    SpecObjectAttribute,
    SpecObjectAttributeType,
)

ATTRIBUTE_STRING_TEMPLATE = """\
            <ATTRIBUTE-VALUE-STRING THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-STRING-REF>{definition_ref}</ATTRIBUTE-DEFINITION-STRING-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
"""

ATTRIBUTE_INTEGER_TEMPLATE = """\
            <ATTRIBUTE-VALUE-INTEGER THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-INTEGER-REF>{definition_ref}</ATTRIBUTE-DEFINITION-INTEGER-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-INTEGER>
"""

ATTRIBUTE_REAL_TEMPLATE = """\
            <ATTRIBUTE-VALUE-REAL THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-REAL-REF>{definition_ref}</ATTRIBUTE-DEFINITION-REAL-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-REAL>
"""

ATTRIBUTE_ENUM_VALUE_TEMPLATE = """\
                <ENUM-VALUE-REF>{value}</ENUM-VALUE-REF>
"""
ATTRIBUTE_ENUMERATION_TEMPLATE = """\
            <ATTRIBUTE-VALUE-ENUMERATION>
              <VALUES>
{values}
              </VALUES>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-ENUMERATION-REF>{definition_ref}</ATTRIBUTE-DEFINITION-ENUMERATION-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-ENUMERATION>
"""
ATTRIBUTE_ENUMERATION_TEMPLATE_REVERSE = """\
            <ATTRIBUTE-VALUE-ENUMERATION>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-ENUMERATION-REF>{definition_ref}</ATTRIBUTE-DEFINITION-ENUMERATION-REF>
              </DEFINITION>
              <VALUES>
{values}
              </VALUES>
            </ATTRIBUTE-VALUE-ENUMERATION>
"""

ATTRIBUTE_DATE_TEMPLATE = """\
            <ATTRIBUTE-VALUE-DATE THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-DATE-REF>{definition_ref}</ATTRIBUTE-DEFINITION-DATE-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-DATE>
"""

ATTRIBUTE_XHTML_TEMPLATE = """\
            <ATTRIBUTE-VALUE-XHTML>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-XHTML-REF>{definition_ref}</ATTRIBUTE-DEFINITION-XHTML-REF>
              </DEFINITION>
              <THE-VALUE>{value}</THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
"""

ATTRIBUTE_BOOLEAN_TEMPLATE = """\
            <ATTRIBUTE-VALUE-BOOLEAN THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-BOOLEAN-REF>{definition_ref}</ATTRIBUTE-DEFINITION-BOOLEAN-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-BOOLEAN>
"""


class SpecObjectParser:
    @staticmethod
    def parse(spec_object_xml) -> ReqIFSpecObject:
        assert "SPEC-OBJECT" in spec_object_xml.tag
        xml_attributes = spec_object_xml.attrib

        spec_object_description: Optional[str] = (
            xml_attributes["DESC"] if "DESC" in xml_attributes else None
        )
        try:
            identifier = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None
        spec_object_last_change: Optional[str] = (
            xml_attributes["LAST-CHANGE"]
            if "LAST-CHANGE" in xml_attributes
            else None
        )
        spec_object_long_name: Optional[str] = (
            xml_attributes["LONG-NAME"]
            if "LONG-NAME" in xml_attributes
            else None
        )

        spec_object_type = (
            spec_object_xml.find("TYPE").find("SPEC-OBJECT-TYPE-REF").text
        )

        xml_spec_values = spec_object_xml.find("VALUES")
        attributes: List[SpecObjectAttribute] = []
        for attribute_xml in xml_spec_values:
            if attribute_xml.tag == "ATTRIBUTE-VALUE-STRING":
                attribute_value = attribute_xml.attrib["THE-VALUE"]
                attribute_definition_ref = attribute_xml[0][0].text
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.STRING,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-ENUMERATION":
                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-ENUMERATION-REF")
                    .text
                )
                attribute_xml_values = attribute_xml.find("VALUES")
                assert attribute_xml_values is not None
                xml_enum_value_refs = attribute_xml_values.getchildren()
                enum_value_refs: List[str] = []
                for xml_enum_value_ref in xml_enum_value_refs:
                    attribute_value = xml_enum_value_ref.text
                    enum_value_refs.append(attribute_value)
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.ENUMERATION,
                    definition_ref=attribute_definition_ref,
                    value=enum_value_refs,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-INTEGER":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-INTEGER-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.INTEGER,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-REAL":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-REAL-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.REAL,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-BOOLEAN":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-BOOLEAN-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.BOOLEAN,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-DATE":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-DATE-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.DATE,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-XHTML":
                the_value = attribute_xml.find("THE-VALUE")

                # Edge case: There are no <xhtml:...> or <reqif-xhtml...> tags.
                if len(the_value.nsmap) > 0:
                    attribute_value = lxml_stringify_namespaced_children(
                        the_value
                    )
                    attribute_value_stripped_xhtml = (
                        reqif_unindent_xhtml_string(
                            lxml_convert_children_from_reqif_ns_xhtml_string(
                                the_value
                            )
                        )
                    )
                else:
                    attribute_value = lxml_stringify_children(the_value)
                    attribute_value_stripped_xhtml = (
                        reqif_unindent_xhtml_string(attribute_value)
                    )
                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-XHTML-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    attribute_type=SpecObjectAttributeType.XHTML,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
                    value_stripped_xhtml=attribute_value_stripped_xhtml,
                    xml_node=attribute_xml,
                )
            else:
                raise NotImplementedError(etree.tostring(attribute_xml))
            attributes.append(attribute)

        return ReqIFSpecObject(
            xml_node=spec_object_xml,
            description=spec_object_description,
            identifier=identifier,
            last_change=spec_object_last_change,
            long_name=spec_object_long_name,
            spec_object_type=spec_object_type,
            attributes=attributes,
        )

    @staticmethod
    def unparse(spec_object: ReqIFSpecObject) -> str:
        output = ""

        output += "        <SPEC-OBJECT"
        if spec_object.description is not None:
            output += f' DESC="{spec_object.description}"'

        output += f' IDENTIFIER="{spec_object.identifier}"'

        if spec_object.last_change:
            output += f' LAST-CHANGE="{spec_object.last_change}"'
        if spec_object.long_name is not None:
            output += f' LONG-NAME="{spec_object.long_name}"'
        output += ">\n"

        if spec_object.xml_node is not None:
            children_tags = list(
                map(lambda el: el.tag, list(spec_object.xml_node))
            )
            assert "VALUES" in children_tags
            assert "TYPE" in children_tags
        else:
            children_tags = ["VALUES", "TYPE"]

        for child_tag in children_tags:
            if child_tag == "VALUES":
                output += SpecObjectParser._unparse_spec_values(spec_object)
            elif child_tag == "TYPE":
                output += SpecObjectParser._unparse_spec_object_type(
                    spec_object
                )
            else:
                print(f"warning: Unknown child tag: {child_tag}.")  # noqa: T201

        output += "        </SPEC-OBJECT>\n"

        return output

    @staticmethod
    def _unparse_spec_object_type(spec_object: ReqIFSpecObject):
        output = ""
        output += (
            "          <TYPE>\n"
            f"            "
            f"<SPEC-OBJECT-TYPE-REF>"
            f"{spec_object.spec_object_type}"
            f"</SPEC-OBJECT-TYPE-REF>\n"
            "          </TYPE>\n"
        )
        return output

    @staticmethod
    def _unparse_spec_values(spec_object: ReqIFSpecObject):
        output = ""
        output += "          <VALUES>\n"
        for attribute in spec_object.attributes:
            if attribute.attribute_type == SpecObjectAttributeType.STRING:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_STRING_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=html.escape(attribute.value),
                )
            elif attribute.attribute_type == SpecObjectAttributeType.INTEGER:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_INTEGER_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.REAL:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_REAL_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif (
                attribute.attribute_type == SpecObjectAttributeType.ENUMERATION
            ):
                if attribute.xml_node is not None:
                    children_tags = list(
                        map(lambda el: el.tag, list(attribute.xml_node))
                    )
                else:
                    children_tags = ["VALUES", "DEFINITION"]
                enum_values_then_definition_order = children_tags.index(
                    "VALUES"
                ) < children_tags.index("DEFINITION")

                assert enum_values_then_definition_order is not None
                assert isinstance(attribute.value, list)
                enum_values: str = "".join(
                    list(
                        map(
                            lambda v: ATTRIBUTE_ENUM_VALUE_TEMPLATE.format(
                                value=v
                            ),
                            attribute.value,
                        )
                    )
                ).rstrip()

                if enum_values_then_definition_order:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE.format(
                        definition_ref=attribute.definition_ref,
                        values=enum_values,
                    )
                else:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE_REVERSE.format(
                        definition_ref=attribute.definition_ref,
                        values=enum_values,
                    )
            elif attribute.attribute_type == SpecObjectAttributeType.DATE:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_DATE_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.XHTML:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_XHTML_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.BOOLEAN:
                assert isinstance(attribute.value, str)
                output += ATTRIBUTE_BOOLEAN_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            else:
                raise NotImplementedError(attribute)

        output += "          </VALUES>\n"
        return output
