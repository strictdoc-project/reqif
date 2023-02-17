from typing import List, Optional

from reqif.helpers.lxml import lxml_is_self_closed_tag
from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)


class ReqIFSpecHierarchyParser:
    @staticmethod
    def parse(spec_hierarchy_xml, level=1) -> ReqIFSpecHierarchy:
        assert spec_hierarchy_xml.tag == "SPEC-HIERARCHY"
        is_self_closed = False
        attributes = spec_hierarchy_xml.attrib
        try:
            identifier = attributes["IDENTIFIER"]
        except Exception:
            raise NotImplementedError from None
        last_change: Optional[str] = (
            attributes["LAST-CHANGE"] if "LAST-CHANGE" in attributes else None
        )
        long_name: Optional[str] = (
            attributes["LONG-NAME"] if "LONG-NAME" in attributes else None
        )
        editable: Optional[bool] = None
        if "IS-EDITABLE" in attributes:
            editable_str = attributes["IS-EDITABLE"]
            editable = editable_str == "true"
        is_table_internal: Optional[bool] = None
        if "IS-TABLE-INTERNAL" in attributes:
            is_table_internal_str = attributes["IS-TABLE-INTERNAL"]
            is_table_internal = is_table_internal_str == "true"

        ref_then_children_order = list(
            map(lambda el: el.tag, list(spec_hierarchy_xml))
        ) == ["OBJECT", "CHILDREN"]

        object_xml = spec_hierarchy_xml.find("OBJECT")
        spec_object_ref_xml = object_xml.find("SPEC-OBJECT-REF")

        spec_object_ref = spec_object_ref_xml.text

        spec_hierarchy_children: Optional[List[ReqIFSpecHierarchy]] = None
        xml_spec_hierarchy_children = spec_hierarchy_xml.find("CHILDREN")
        if xml_spec_hierarchy_children is not None:
            spec_hierarchy_children = []
            if len(xml_spec_hierarchy_children) == 0:
                is_self_closed = lxml_is_self_closed_tag(
                    xml_spec_hierarchy_children
                )
            for child_spec_hierarchy_xml in xml_spec_hierarchy_children:
                child_spec_hierarchy = ReqIFSpecHierarchyParser.parse(
                    child_spec_hierarchy_xml, level + 1
                )
                spec_hierarchy_children.append(child_spec_hierarchy)
        return ReqIFSpecHierarchy(
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
            editable=editable,
            spec_object=spec_object_ref,
            children=spec_hierarchy_children,
            ref_then_children_order=ref_then_children_order,
            level=level,
            is_table_internal=is_table_internal,
            is_self_closed=is_self_closed,
            xml_node=spec_hierarchy_xml,
        )

    @staticmethod
    def unparse(hierarchy: ReqIFSpecHierarchy) -> str:
        base_level = hierarchy.calculate_base_level()
        base_level_str = " " * base_level
        output = (
            base_level_str + f"<SPEC-HIERARCHY"
            f' IDENTIFIER="{hierarchy.identifier}"'
        )
        if hierarchy.editable is not None:
            editable_value = "true" if hierarchy.editable else "false"
            output += f' IS-EDITABLE="{editable_value}"'
        if hierarchy.is_table_internal is not None:
            is_table_internal_value = (
                "true" if hierarchy.is_table_internal else "false"
            )
            output += f' IS-TABLE-INTERNAL="{is_table_internal_value}"'
        if hierarchy.last_change:
            output += f' LAST-CHANGE="{hierarchy.last_change}"'
        if hierarchy.long_name:
            output += f' LONG-NAME="{hierarchy.long_name}"'
        output += ">\n"

        def print_object():
            object_output = base_level_str + "  <OBJECT>\n"
            object_output += (
                base_level_str + "    "
                f"<SPEC-OBJECT-REF>{hierarchy.spec_object}</SPEC-OBJECT-REF>\n"
            )
            object_output += base_level_str + "  </OBJECT>\n"
            return object_output

        def print_children():
            children_output = ""
            if len(hierarchy.children) == 0:
                if hierarchy.is_self_closed:
                    children_output += base_level_str + "  <CHILDREN/>\n"
                    return children_output
            children_output += base_level_str + "  <CHILDREN>\n"
            for child in hierarchy.children:
                children_output += ReqIFSpecHierarchyParser.unparse(child)
            children_output += base_level_str + "  </CHILDREN>\n"
            return children_output

        if hierarchy.ref_then_children_order:
            output += print_object()
            if hierarchy.children is not None:
                output += print_children()
        else:
            if hierarchy.children is not None:
                output += print_children()
            output += print_object()

        output += base_level_str + "</SPEC-HIERARCHY>\n"

        return output
