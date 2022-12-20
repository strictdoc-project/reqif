from typing import List, Optional

import lxml

from reqif.models.reqif_spec_object import SpecObjectAttribute
from reqif.models.reqif_specification import (
    ReqIFSpecification,
)
from reqif.models.reqif_types import SpecObjectAttributeType
from reqif.parsers.spec_hierarchy_parser import (
    ReqIFSpecHierarchyParser,
)
from reqif.parsers.spec_object_parser import (
    ATTRIBUTE_XHTML_TEMPLATE,
    ATTRIBUTE_DATE_TEMPLATE,
)


class ReqIFSpecificationParser:
    @staticmethod
    def parse(specification_xml):
        assert "SPECIFICATION" in specification_xml.tag, f"{specification_xml}"

        attributes = specification_xml.attrib
        try:
            identifier = attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError(attributes) from None

        # DESC is optional
        description: Optional[str] = (
            attributes["DESC"] if "DESC" in attributes else None
        )

        # LAST-CHANGE is optional
        last_change: Optional[str] = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )

        # LONG-NAME is optional
        long_name: Optional[str] = (
            attributes["LONG-NAME"] if "LONG-NAME" in attributes else None
        )

        specification_type: Optional[str] = None
        xml_specification_type = specification_xml.find("TYPE")
        if xml_specification_type is not None:
            xml_specification_type_ref = xml_specification_type.find(
                "SPECIFICATION-TYPE-REF"
            )
            if xml_specification_type_ref is not None:
                specification_type = xml_specification_type_ref.text

        specification_children_xml = list(specification_xml)
        children_xml = None
        for specification_child_xml in specification_children_xml:
            if specification_child_xml.tag == "TYPE":
                pass  # type_xml = specification_child_xml
            elif specification_child_xml.tag == "CHILDREN":
                children_xml = specification_child_xml

        children = None
        if children_xml is not None:
            children = []
            for child_xml in children_xml:
                spec_hierarchy_xml = ReqIFSpecHierarchyParser.parse(child_xml)
                children.append(spec_hierarchy_xml)

        values: Optional[List[SpecObjectAttribute]] = None
        xml_values = specification_xml.find("VALUES")
        if xml_values is not None:
            values = []
            if len(xml_values) > 0:
                xml_attribute = xml_values[0]
                if xml_attribute.tag == "ATTRIBUTE-VALUE-STRING":
                    attribute_value = xml_attribute.attrib["THE-VALUE"]
                    definition_ref = xml_attribute[0][0].text
                    values_attribute = SpecObjectAttribute(
                        xml_node=xml_attribute,
                        attribute_type=SpecObjectAttributeType.STRING,
                        definition_ref=definition_ref,
                        value=attribute_value,
                    )
                    values.append(values_attribute)
                if xml_attribute.tag == "ATTRIBUTE-VALUE-DATE":
                    attribute_value = xml_attribute.attrib["THE-VALUE"]
                    definition_ref = xml_attribute[0][0].text
                    values_attribute = SpecObjectAttribute(
                        xml_node=xml_attribute,
                        attribute_type=SpecObjectAttributeType.DATE,
                        definition_ref=definition_ref,
                        value=attribute_value,
                    )
                    values.append(values_attribute)
                elif xml_attribute.tag == "ATTRIBUTE-VALUE-XHTML":
                    the_value = xml_attribute.find("THE-VALUE")
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
                    attribute_name = (
                        xml_attribute.find("DEFINITION")
                        .find("ATTRIBUTE-DEFINITION-XHTML-REF")
                        .text
                    )
                    values_attribute = SpecObjectAttribute(
                        xml_node=xml_attribute,
                        attribute_type=SpecObjectAttributeType.XHTML,
                        definition_ref=attribute_name,
                        value=attribute_value,
                    )
                    values.append(values_attribute)
                else:
                    raise NotImplementedError(xml_attribute)
        return ReqIFSpecification(
            xml_node=specification_xml,
            description=description,
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
            values=values,
            specification_type=specification_type,
            children=children,
        )

    @staticmethod
    def unparse(specification: ReqIFSpecification) -> str:
        output = ""

        output += "        <SPECIFICATION"
        if specification.description is not None:
            output += f' DESC="{specification.description}"'

        output += f' IDENTIFIER="{specification.identifier}"'

        if specification.last_change is not None:
            output += f' LAST-CHANGE="{specification.last_change}"'
        if specification.long_name:
            output += f' LONG-NAME="{specification.long_name}"'
        output += ">\n"

        if specification.xml_node is not None:
            children_tags = list(
                map(lambda el: el.tag, list(specification.xml_node))
            )
        else:
            children_tags = ["TYPE", "CHILDREN", "VALUES"]

        for tag in children_tags:
            if tag == "TYPE":
                if specification.specification_type:
                    output += (
                        ReqIFSpecificationParser._unparse_specification_type(
                            specification
                        )
                    )
            elif tag == "CHILDREN":
                if specification.children is not None:
                    # fmt: off
                    output += (
                        ReqIFSpecificationParser
                        ._unparse_specification_children(
                            specification
                        )
                    )
                    # fmt: on
            elif tag == "VALUES":
                xml_values_attributes = specification.values
                if xml_values_attributes is not None:
                    if len(xml_values_attributes) == 0:
                        output += "          <VALUES/>\n"
                    else:
                        output += "          <VALUES>\n"
                        for xml_attribute in xml_values_attributes:
                            if (
                                xml_attribute.attribute_type
                                == SpecObjectAttributeType.DATE
                            ):
                                output += ATTRIBUTE_DATE_TEMPLATE.format(
                                    definition_ref=xml_attribute.definition_ref,
                                    value=xml_attribute.value,
                                )
                            elif (
                                xml_attribute.attribute_type
                                == SpecObjectAttributeType.XHTML
                            ):
                                output += ATTRIBUTE_XHTML_TEMPLATE.format(
                                    definition_ref=xml_attribute.definition_ref,
                                    value=xml_attribute.value,
                                )
                            else:
                                raise NotImplementedError(xml_attribute)
                        output += "          </VALUES>\n"
        output += "        </SPECIFICATION>\n"

        return output

    @staticmethod
    def _unparse_specification_type(specification: ReqIFSpecification):
        output = ""
        output += (
            "          <TYPE>\n"
            "            <SPECIFICATION-TYPE-REF>"
            f"{specification.specification_type}"
            "</SPECIFICATION-TYPE-REF>\n"
            "          </TYPE>\n"
        )
        return output

    @staticmethod
    def _unparse_specification_children(specification: ReqIFSpecification):
        output = ""
        output += "          <CHILDREN>\n"

        specification_children = specification.children
        if specification_children is not None:
            for hierarchy in specification_children:
                output += ReqIFSpecHierarchyParser.unparse(hierarchy)

        output += "          </CHILDREN>\n"
        return output
