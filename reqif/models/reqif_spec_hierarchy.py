from typing import Any, List, Optional

from reqif.helpers.debug import auto_described


@auto_described
class ReqIFSpecHierarchy:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        identifier: str,
        spec_object: str,
        level: int,
        children: Optional[List] = None,
        long_name: Optional[str] = None,
        ref_then_children_order: bool = True,
        last_change: Optional[str] = None,
        editable: Optional[bool] = False,
        is_table_internal: Optional[bool] = False,
        is_self_closed: bool = True,
        xml_node: Optional[Any] = None,
    ):
        assert level >= 0

        # Mandatory fields.
        self.identifier: str = identifier
        self.spec_object: str = spec_object
        # Not part of ReqIF, but helpful to calculate the section depth levels.
        self.level = level

        # Optional fields.
        self.children: Optional[List] = children
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
        assert (self.level + 1) == spec_hierarchy.level, (
            f"Broken parent-child level relationship.\n"
            f"Parent: {self}\nChild: {spec_hierarchy}"
        )
        self.children.append(spec_hierarchy)

    def calculate_base_level(self) -> int:
        assert self.level > 0, f"{self.level}"
        return 12 + (self.level - 1) * 4
