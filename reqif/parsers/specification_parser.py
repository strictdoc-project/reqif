from typing import List, Optional

from reqif.helpers.lxml import lxml_escape_for_html
from reqif.models.reqif_spec_object import SpecObjectAttribute
from reqif.models.reqif_specification import (
    ReqIFSpecification,
)
from reqif.parsers.attribute_value_parser import AttributeValueParser
from reqif.parsers.spec_hierarchy_parser import (
    ReqIFSpecHierarchyParser,
)


class ReqIFSpecificationParser:
    @staticmethod
    def parse(specification_xml) -> ReqIFSpecification:
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

        xml_spec_values = specification_xml.find("VALUES")
        values: Optional[
            List[SpecObjectAttribute]
        ] = AttributeValueParser.parse_attribute_values(xml_spec_values)

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
            escaped_description = lxml_escape_for_html(
                specification.description
            )
            output += f' DESC="{escaped_description}"'

        output += f' IDENTIFIER="{specification.identifier}"'

        if specification.last_change is not None:
            output += f' LAST-CHANGE="{specification.last_change}"'
        if specification.long_name is not None:
            escaped_long_name = lxml_escape_for_html(specification.long_name)
            output += f' LONG-NAME="{escaped_long_name}"'

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
                output += AttributeValueParser.unparse_attribute_values(
                    specification.values
                )
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
