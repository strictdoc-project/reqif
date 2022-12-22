import html
from typing import List, Optional

import lxml
from lxml import etree

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

ATTRIBUTE_ENUMERATION_TEMPLATE = """\
            <ATTRIBUTE-VALUE-ENUMERATION>
              <VALUES>
                <ENUM-VALUE-REF>{value}</ENUM-VALUE-REF>
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
                <ENUM-VALUE-REF>{value}</ENUM-VALUE-REF>
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
              <THE-VALUE>
{value}
              </THE-VALUE>
            </ATTRIBUTE-VALUE-XHTML>
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
                attribute_value = (
                    attribute_xml.find("VALUES").find("ENUM-VALUE-REF").text
                )
                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-ENUMERATION-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.ENUMERATION,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
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
                # TODO: This does not work:
                # <THE-VALUE xmlns:xhtml="http://www.w3.org/1999/xhtml">
                # is printed.
                # the_value.tag = etree.QName(the_value).localname
                # etree.cleanup_namespaces(the_value)
                attribute_value_decoded_lines = (
                    lxml.etree.tostring(the_value, method="xml")
                    .decode("utf8")
                    .rstrip()
                )
                attribute_value = "\n".join(
                    attribute_value_decoded_lines.split("\n")[1:-1]
                )
                attribute_definition_ref = (
                    attribute_xml.find("DEFINITION")
                    .find("ATTRIBUTE-DEFINITION-XHTML-REF")
                    .text
                )
                attribute = SpecObjectAttribute(
                    xml_node=attribute_xml,
                    attribute_type=SpecObjectAttributeType.XHTML,
                    definition_ref=attribute_definition_ref,
                    value=attribute_value,
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
            assert len(children_tags) == 2
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
                raise NotImplementedError

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
            attribute_value = html.escape(attribute.value)
            if attribute.attribute_type == SpecObjectAttributeType.STRING:
                output += ATTRIBUTE_STRING_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute_value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.INTEGER:
                output += ATTRIBUTE_INTEGER_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.REAL:
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
                if enum_values_then_definition_order:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE.format(
                        definition_ref=attribute.definition_ref,
                        value=attribute.value,
                    )
                else:
                    output += ATTRIBUTE_ENUMERATION_TEMPLATE_REVERSE.format(
                        definition_ref=attribute.definition_ref,
                        value=attribute.value,
                    )
            elif attribute.attribute_type == SpecObjectAttributeType.DATE:
                output += ATTRIBUTE_DATE_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            elif attribute.attribute_type == SpecObjectAttributeType.XHTML:
                output += ATTRIBUTE_XHTML_TEMPLATE.format(
                    definition_ref=attribute.definition_ref,
                    value=attribute.value,
                )
            else:
                raise NotImplementedError(attribute)

        output += "          </VALUES>\n"
        return output
