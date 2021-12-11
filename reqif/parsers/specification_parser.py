from typing import List

from reqif.models.reqif_spec_hierarchy import ReqIFSpecHierarchy
from reqif.models.reqif_specification import (
    ReqIFSpecification,
)
from reqif.parsers.spec_hierarchy_parser import (
    ReqIFSpecHierarchyParser,
)
from reqif.specification_iterator import SpecificationIterator


class ReqIFSpecificationParser:
    @staticmethod
    def parse(specification_xml):
        assert "SPECIFICATION" in specification_xml.tag, f"{specification_xml}"
        attributes = specification_xml.attrib
        try:
            identifier = attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError(specification_xml) from None
        try:
            long_name = attributes["LONG-NAME"]
        except Exception:
            raise NotImplementedError(specification_xml) from None

        try:
            specification_type = (
                specification_xml.find("TYPE")
                .find("SPECIFICATION-TYPE-REF")
                .text
            )
        except Exception:
            raise NotImplementedError(specification_xml) from None

        specification_children_xml = list(specification_xml)
        # type_xml = None
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
            long_name=long_name,
            specification_type=specification_type,
            children=children,
        )

    @staticmethod
    def unparse(specification: ReqIFSpecification) -> str:
        output = ""

        output += (
            "        <SPECIFICATION "
            f'IDENTIFIER="{specification.identifier}" '
            'LAST-CHANGE="2021-10-14T10:11:59.495+02:00" '
            f'LONG-NAME="{specification.long_name}">\n'
        )

        output += f"""\
          <VALUES/>
          <TYPE>
            <SPECIFICATION-TYPE-REF>\
{specification.specification_type}\
</SPECIFICATION-TYPE-REF>
          </TYPE>
"""

        output += "          <CHILDREN>\n"

        closing_tags: List[ReqIFSpecHierarchy] = []
        for current_hierarchy in SpecificationIterator.iterate_specification(
            specification
        ):
            while (
                len(closing_tags) > 0
                and current_hierarchy.level <= closing_tags[-1].level
            ):
                hierarchy = closing_tags.pop()
                output += ReqIFSpecificationParser.print_closing_tag(hierarchy)

            output += ReqIFSpecificationParser.print_spec_hierarchy(
                current_hierarchy
            )
            closing_tags.append(current_hierarchy)

        while len(closing_tags) > 0:
            hierarchy = closing_tags.pop()
            output += ReqIFSpecificationParser.print_closing_tag(hierarchy)

        output += "          </CHILDREN>\n"

        output += "        </SPECIFICATION>\n"

        return output

    @staticmethod
    def print_spec_hierarchy(hierarchy: ReqIFSpecHierarchy) -> str:
        base_level = 10 + hierarchy.level * 2
        base_level_str = " " * base_level
        output = (
            base_level_str + f"<SPEC-HIERARCHY "
            f'IDENTIFIER="{hierarchy.identifier}" '
            f'LAST-CHANGE="2021-10-15T09:21:00.153+02:00">\n'
        )

        output += base_level_str + "  <OBJECT>\n"
        output += (
            base_level_str + "    "
            f"<SPEC-OBJECT-REF>{hierarchy.spec_object}</SPEC-OBJECT-REF>\n"
        )
        output += base_level_str + "  </OBJECT>\n"

        if hierarchy.children is not None:
            output += base_level_str + "  <CHILDREN>\n"

        return output

    @staticmethod
    def print_closing_tag(hierarchy: ReqIFSpecHierarchy) -> str:
        base_level = 10 + hierarchy.level * 2
        base_level_str = " " * base_level

        output = ""

        if hierarchy.children is not None:
            output += base_level_str + "  </CHILDREN>\n"

        output += base_level_str
        output += "</SPEC-HIERARCHY>\n"
        # output += " " * (10 + level * 2)
        # output += "</CHILDREN>\n"

        return output
