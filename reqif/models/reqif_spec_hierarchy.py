from typing import Any, List, Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_types import SpecObjectAttributeType


@auto_described
class EditableAttributeRef:
    """One entry of a SPEC-HIERARCHY <EDITABLE-ATTS> element.

    The attribute type is carried alongside the reference because the reference
    tag names it: ATTRIBUTE-DEFINITION-STRING-REF, -INTEGER-REF, and so on. It
    cannot be recovered from the identifier alone.
    """

    def __init__(
        self,
        *,
        attribute_type: SpecObjectAttributeType,
        definition_ref: str,
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.definition_ref: str = definition_ref


@auto_described
class ReqIFSpecHierarchy:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        identifier: str,
        spec_object: str,
        level: int,
        children: Optional[List["ReqIFSpecHierarchy"]] = None,
        description: Optional[str] = None,
        editable_atts: Optional[List[EditableAttributeRef]] = None,
        long_name: Optional[str] = None,
        ref_then_children_order: bool = True,
        last_change: Optional[str] = None,
        editable: Optional[bool] = False,
        is_table_internal: Optional[bool] = False,
        is_self_closed: bool = True,
        xml_node: Optional[Any] = None,
        alternative_id: Optional[str] = None,
    ):
        assert level >= 0

        # Mandatory fields.
        self.identifier: str = identifier
        self.alternative_id: Optional[str] = alternative_id
        self.spec_object: str = spec_object
        # Not part of ReqIF, but helpful to calculate the section depth levels.
        self.level = level

        # Optional fields
        self.children: Optional[List[ReqIFSpecHierarchy]] = children
        self.description: Optional[str] = description
        self.editable_atts: Optional[List[EditableAttributeRef]] = editable_atts
        self.long_name: Optional[str] = long_name
        # Not part of REqIF, but helpful for printing the
        # <OBJECT> and <CHILDREN> tags depending on which tool produced the
        # ReqIF file.
        self.ref_then_children_order: bool = ref_then_children_order
        self.last_change: Optional[str] = last_change
        self.editable: Optional[bool] = editable
        self.is_table_internal: Optional[bool] = is_table_internal
        self.is_self_closed: bool = is_self_closed
        self.xml_node = xml_node

    def add_child(self, spec_hierarchy):
        if self.children is None:
            self.children = []
        assert (self.level + 1) == spec_hierarchy.level, (
            f"Broken parent-child level relationship.\n"
            f"Parent: {self}\nChild: {spec_hierarchy}"
        )
        self.children.append(spec_hierarchy)

    def calculate_base_level(self) -> int:
        assert self.level > 0, f"{self.level}"
        return 12 + (self.level - 1) * 4
