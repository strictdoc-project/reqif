from typing import List, Optional

from reqif.models.reqif_specification import (
    ReqIFSpecification,
)
from reqif.parsers.spec_hierarchy_parser import (
    ReqIFSpecHierarchyParser,
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

        # LAST-CHANGE is optional
        last_change = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )

        # LONG-NAME is optional
        long_name = (
            attributes["LONG-NAME"] if "LONG-NAME" in attributes else None
        )

        values: Optional[List] = None
        xml_values = specification_xml.find("VALUES")
        if xml_values is not None:
            if len(xml_values) != 0:
                raise NotImplementedError(xml_values)
            values = []

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
        assert children_xml is not None

        children = []
        if children_xml is not None and len(children_xml):
            for child_xml in children_xml:
                spec_hierarchy_xml = ReqIFSpecHierarchyParser.parse(child_xml)
                children.append(spec_hierarchy_xml)
        return ReqIFSpecification(
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

        output += (
            f'        <SPECIFICATION IDENTIFIER="{specification.identifier}"'
        )
        if specification.last_change is not None:
            output += f' LAST-CHANGE="{specification.last_change}"'
        if specification.long_name:
            output += f' LONG-NAME="{specification.long_name}"'
        output += ">\n"

        specification_values = specification.values
        if specification_values is not None:
            if len(specification_values) != 0:
                raise NotImplementedError(specification_values)
            output += "          <VALUES/>\n"

        if specification.specification_type:
            output += f"""\
          <TYPE>
            <SPECIFICATION-TYPE-REF>\
{specification.specification_type}\
</SPECIFICATION-TYPE-REF>
          </TYPE>
"""

        output += "          <CHILDREN>\n"

        for hierarchy in specification.children:
            output += ReqIFSpecHierarchyParser.unparse(hierarchy)

        output += "          </CHILDREN>\n"
        output += "        </SPECIFICATION>\n"

        return output
