from typing import List, Optional

from lxml import etree

from reqif.helpers.lxml import stringify_children
from reqif.models.reqif_spec_object import (
    ReqIFSpecObject,
    SpecObjectAttribute,
    SpecObjectAttributeType,
)


ATTRIBUTE_STRING_TEMPLATE = """\
            <ATTRIBUTE-VALUE-STRING THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-STRING-REF>{name}</ATTRIBUTE-DEFINITION-STRING-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-STRING>
"""

ATTRIBUTE_INTEGER_TEMPLATE = """\
            <ATTRIBUTE-VALUE-INTEGER THE-VALUE="{value}">
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-INTEGER-REF>{name}</ATTRIBUTE-DEFINITION-INTEGER-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-INTEGER>
"""

ATTRIBUTE_ENUMERATION_TEMPLATE = """\
            <ATTRIBUTE-VALUE-ENUMERATION>
              <VALUES>
                <ENUM-VALUE-REF>{value}</ENUM-VALUE-REF>
              </VALUES>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-ENUMERATION-REF>{name}</ATTRIBUTE-DEFINITION-ENUMERATION-REF>
              </DEFINITION>
            </ATTRIBUTE-VALUE-ENUMERATION>
"""
ATTRIBUTE_ENUMERATION_TEMPLATE_REVERSE = """\
            <ATTRIBUTE-VALUE-ENUMERATION>
              <DEFINITION>
                <ATTRIBUTE-DEFINITION-ENUMERATION-REF>{name}</ATTRIBUTE-DEFINITION-ENUMERATION-REF>
              </DEFINITION>
              <VALUES>
                <ENUM-VALUE-REF>{value}</ENUM-VALUE-REF>
              </VALUES>
            </ATTRIBUTE-VALUE-ENUMERATION>
"""


class SpecObjectParser:
    @staticmethod
    def parse(spec_object_xml) -> ReqIFSpecObject:
        assert "SPEC-OBJECT" in spec_object_xml.tag
        xml_attributes = spec_object_xml.attrib

        children_tags = list(map(lambda el: el.tag, list(spec_object_xml)))
        assert len(children_tags) == 2
        values_then_type_order = children_tags == ["VALUES", "TYPE"]

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
        attribute_map = {}
        for attribute_xml in xml_spec_values:
            if attribute_xml.tag == "ATTRIBUTE-VALUE-STRING":
                attribute_value = attribute_xml.attrib["THE-VALUE"]
                attribute_name = attribute_xml[0][0].text
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.STRING,
                    attribute_name,
                    attribute_value,
                    enum_values_then_definition_order=None,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-ENUMERATION":
                children_tags = list(
                    map(lambda el: el.tag, list(attribute_xml))
                )
                enum_values_then_definition_order = children_tags.index(
                    "VALUES"
                ) < children_tags.index("DEFINITION")

                attribute_value = (
                    attribute_xml.find("VALUES").find("ENUM-VALUE-REF").text
                )
                attribute_name = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-ENUMERATION-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.ENUMERATION,
                    attribute_name,
                    attribute_value,
                    enum_values_then_definition_order,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-INTEGER":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_name = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-INTEGER-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.INTEGER,
                    attribute_name,
                    attribute_value,
                    enum_values_then_definition_order=None,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-BOOLEAN":
                attribute_value = attribute_xml.attrib["THE-VALUE"]

                attribute_name = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-BOOLEAN-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.BOOLEAN,
                    attribute_name,
                    attribute_value,
                    enum_values_then_definition_order=None,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-XHTML":
                attribute_value = stringify_children(
                    attribute_xml.find("THE-VALUE")
                )
                attribute_name = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-XHTML-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.XHTML,
                    attribute_name,
                    attribute_value,
                    enum_values_then_definition_order=None,
                )
            else:
                raise NotImplementedError(etree.tostring(attribute_xml))
            attributes.append(attribute)
            attribute_map[attribute_name] = attribute_value

        return ReqIFSpecObject(
            description=spec_object_description,
            identifier=identifier,
            last_change=spec_object_last_change,
            long_name=spec_object_long_name,
            spec_object_type=spec_object_type,
            attributes=attributes,
            attribute_map=attribute_map,
            values_then_type_order=values_then_type_order,
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

        if spec_object.values_then_type_order:
            output += SpecObjectParser._unparse_spec_values(spec_object)
            output += SpecObjectParser._unparse_spec_object_type(spec_object)
        else:
            output += SpecObjectParser._unparse_spec_object_type(spec_object)
            output += SpecObjectParser._unparse_spec_values(spec_object)

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
                output += ATTRIBUTE_STRING_TEMPLATE.format(
                    name=attribute.name, value=attribute.value
                )
            elif attribute.attribute_type == SpecObjectAttributeType.INTEGER:
                output += ATTRIBUTE_INTEGER_TEMPLATE.format(
                    name=attribute.name, value=attribute.value
                )
            elif (
                attribute.attribute_type == SpecObjectAttributeType.ENUMERATION
            ):
                assert attribute.enum_values_then_definition_order is not None
                if attribute.enum_values_then_definition_order:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE.format(
                        name=attribute.name, value=attribute.value
                    )
                else:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE_REVERSE.format(
                        name=attribute.name, value=attribute.value
                    )
        output += "          </VALUES>\n"
        return output
