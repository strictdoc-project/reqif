from typing import List

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


class SpecObjectParser:
    @staticmethod
    def parse(spec_object_xml) -> ReqIFSpecObject:
        assert "SPEC-OBJECT" in spec_object_xml.tag
        xml_attributes = spec_object_xml.attrib

        try:
            identifier = xml_attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None

        spec_object_type = (
            spec_object_xml.find("TYPE").find("SPEC-OBJECT-TYPE-REF").text
        )

        attributes: List[SpecObjectAttribute] = []
        attribute_map = {}
        for attribute_xml in spec_object_xml[0]:
            if attribute_xml.tag == "ATTRIBUTE-VALUE-STRING":
                attribute_value = attribute_xml.attrib["THE-VALUE"]
                attribute_name = attribute_xml[0][0].text
                attribute = SpecObjectAttribute(
                    SpecObjectAttributeType.STRING,
                    attribute_name,
                    attribute_value,
                )
            elif attribute_xml.tag == "ATTRIBUTE-VALUE-ENUMERATION":
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
                )
            else:
                raise NotImplementedError(etree.tostring(attribute_xml))
            attributes.append(attribute)
            attribute_map[attribute_name] = attribute_value

        return ReqIFSpecObject(
            identifier, spec_object_type, attributes, attribute_map
        )

    @staticmethod
    def unparse(spec_object: ReqIFSpecObject) -> str:
        output = ""

        output += (
            "        <SPEC-OBJECT "
            f'IDENTIFIER="{spec_object.identifier}" '
            'LAST-CHANGE="2021-10-15T11:34:36.007+02:00">\n'
        )
        output += "          <VALUES>\n"
        for attribute in spec_object.attributes:
            if attribute.attribute_type == SpecObjectAttributeType.STRING:
                output += ATTRIBUTE_STRING_TEMPLATE.format(
                    name=attribute.name, value=attribute.value
                )
            elif (
                attribute.attribute_type == SpecObjectAttributeType.ENUMERATION
            ):
                output += ATTRIBUTE_ENUMERATION_TEMPLATE.format(
                    name=attribute.name, value=attribute.value
                )
        output += "          </VALUES>\n"
        output += (
            "          <TYPE>\n"
            f"            "
            f"<SPEC-OBJECT-TYPE-REF>"
            f"{spec_object.spec_object_type}"
            f"</SPEC-OBJECT-TYPE-REF>\n"
            "          </TYPE>\n"
        )
        output += "        </SPEC-OBJECT>\n"

        return output
