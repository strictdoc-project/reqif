from typing import Dict, List, Optional

from reqif.helpers.lxml import (
    lxml_escape_for_html,
    lxml_is_comment_node,
    lxml_is_self_closed_tag,
)
from reqif.models.reqif_spec_hierarchy import (
    EditableAttributeRef,
    ReqIFSpecHierarchy,
)
from reqif.models.reqif_types import SpecObjectAttributeType
from reqif.parsers.alternative_id_parser import AlternativeIDParser

# ATTRIBUTE-DEFINITION-STRING-REF -> STRING, and so on for the other six kinds.
# Derived from the enum so the two cannot drift apart.
EDITABLE_ATTS_REF_TAGS: Dict[str, SpecObjectAttributeType] = {
    f"{attribute_type.get_spec_type_tag()}-REF": attribute_type
    for attribute_type in SpecObjectAttributeType
}


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
        description: Optional[str] = (
            attributes["DESC"] if "DESC" in attributes else None
        )
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

        # Only the relative order of OBJECT and CHILDREN matters here. Comparing
        # the whole child list would read any other child, such as ALTERNATIVE-ID,
        # EDITABLE-ATTS or a comment node, as "not the OBJECT-then-CHILDREN shape"
        # and silently swap the two on write.
        ref_then_children_order = [
            el.tag for el in spec_hierarchy_xml if el.tag in ("OBJECT", "CHILDREN")
        ] == ["OBJECT", "CHILDREN"]

        object_xml = spec_hierarchy_xml.find("OBJECT")
        spec_object_ref_xml = object_xml.find("SPEC-OBJECT-REF")

        spec_object_ref = spec_object_ref_xml.text

        editable_atts: Optional[List[EditableAttributeRef]] = None
        xml_editable_atts = spec_hierarchy_xml.find("EDITABLE-ATTS")
        if xml_editable_atts is not None:
            editable_atts = []
            for xml_ref in xml_editable_atts:
                if lxml_is_comment_node(xml_ref):
                    continue
                if xml_ref.tag not in EDITABLE_ATTS_REF_TAGS:
                    raise NotImplementedError(xml_ref.tag)
                editable_atts.append(
                    EditableAttributeRef(
                        attribute_type=EDITABLE_ATTS_REF_TAGS[xml_ref.tag],
                        definition_ref=xml_ref.text,
                    )
                )

        spec_hierarchy_children: Optional[List[ReqIFSpecHierarchy]] = None
        xml_spec_hierarchy_children = spec_hierarchy_xml.find("CHILDREN")
        if xml_spec_hierarchy_children is not None:
            spec_hierarchy_children = []
            if len(xml_spec_hierarchy_children) == 0:
                is_self_closed = lxml_is_self_closed_tag(xml_spec_hierarchy_children)
            for child_spec_hierarchy_xml in xml_spec_hierarchy_children:
                child_spec_hierarchy = ReqIFSpecHierarchyParser.parse(
                    child_spec_hierarchy_xml, level + 1
                )
                spec_hierarchy_children.append(child_spec_hierarchy)
        return ReqIFSpecHierarchy(
            alternative_id=AlternativeIDParser.parse(spec_hierarchy_xml),
            identifier=identifier,
            description=description,
            last_change=last_change,
            long_name=long_name,
            editable=editable,
            spec_object=spec_object_ref,
            children=spec_hierarchy_children,
            editable_atts=editable_atts,
            ref_then_children_order=ref_then_children_order,
            level=level,
            is_table_internal=is_table_internal,
            is_self_closed=is_self_closed,
            xml_node=spec_hierarchy_xml,
        )

    @staticmethod
    def unparse(hierarchy: ReqIFSpecHierarchy) -> str:
        base_level = hierarchy.calculate_base_level()
        base_level_str: str = " " * base_level
        output: str = base_level_str + "<SPEC-HIERARCHY"
        if hierarchy.description is not None:
            escaped_description = lxml_escape_for_html(hierarchy.description)
            output += f' DESC="{escaped_description}"'
        output += f' IDENTIFIER="{hierarchy.identifier}"'
        if hierarchy.editable is not None:
            editable_value = "true" if hierarchy.editable else "false"
            output += f' IS-EDITABLE="{editable_value}"'
        if hierarchy.is_table_internal is not None:
            is_table_internal_value = "true" if hierarchy.is_table_internal else "false"
            output += f' IS-TABLE-INTERNAL="{is_table_internal_value}"'
        if hierarchy.last_change:
            output += f' LAST-CHANGE="{hierarchy.last_change}"'
        if hierarchy.long_name:
            output += f' LONG-NAME="{hierarchy.long_name}"'
        output += ">\n"

        output += AlternativeIDParser.unparse(
            hierarchy.alternative_id, base_level_str + "  "
        )

        # Emitted before OBJECT and CHILDREN, matching the order the schema
        # lists SPEC-HIERARCHY's children in. The element is an xsd:all, so the
        # position carries no meaning, and no existing fixture uses it.
        if hierarchy.editable_atts is not None:
            if len(hierarchy.editable_atts) == 0:
                output += base_level_str + "  <EDITABLE-ATTS/>\n"
            else:
                output += base_level_str + "  <EDITABLE-ATTS>\n"
                for editable_att in hierarchy.editable_atts:
                    ref_tag = f"{editable_att.attribute_type.get_spec_type_tag()}-REF"
                    output += (
                        base_level_str + "    "
                        f"<{ref_tag}>{editable_att.definition_ref}</{ref_tag}>\n"
                    )
                output += base_level_str + "  </EDITABLE-ATTS>\n"

        def print_object() -> str:
            object_output = base_level_str + "  <OBJECT>\n"
            object_output += (
                base_level_str + "    "
                f"<SPEC-OBJECT-REF>{hierarchy.spec_object}</SPEC-OBJECT-REF>\n"
            )
            object_output += base_level_str + "  </OBJECT>\n"
            return object_output

        def print_children(children: List[ReqIFSpecHierarchy]):
            children_output = ""
            if len(children) == 0:
                if hierarchy.is_self_closed:
                    children_output += base_level_str + "  <CHILDREN/>\n"
                    return children_output
            children_output += base_level_str + "  <CHILDREN>\n"
            for child_ in children:
                children_output += ReqIFSpecHierarchyParser.unparse(child_)
            children_output += base_level_str + "  </CHILDREN>\n"
            return children_output

        if hierarchy.ref_then_children_order:
            output += print_object()
            if hierarchy.children is not None:
                output += print_children(hierarchy.children)
        else:
            if hierarchy.children is not None:
                output += print_children(hierarchy.children)
            output += print_object()

        output += base_level_str + "</SPEC-HIERARCHY>\n"

        return output
