from typing import List, Optional

from reqif.helpers.debug import auto_str


class ReqIFSpecHierarchy:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        xml_node,
        is_self_closed: bool,
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        spec_object: str,
        children: Optional[List],
        ref_then_children_order: bool,
        level: int,
    ):
        assert level >= 0

        self.xml_node = xml_node
        self.is_self_closed = is_self_closed
        self.identifier = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name

        self.spec_object = spec_object
        self.children: Optional[List] = children

        # Not part of REqIF, but helpful for printing the
        # <OBJECT> and <CHILDREN> tags depending on which tool produced the
        # ReqIF file.
        self.ref_then_children_order: bool = ref_then_children_order
        # Not part of ReqIF, but helpful to calculate the section depth levels.
        self.level = level

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)

    def add_child(self, spec_hierarchy):
        assert (self.level + 1) == spec_hierarchy.level, (
            f"Broken parent-child level relationship.\n"
            f"Parent: {self.dump()}\nChild: {spec_hierarchy.auto_dump()}"
        )
        self.children.append(spec_hierarchy)

    def dump(self) -> str:
        assert self.level >= 0
        level_str = " " * ((self.level) * 2)
        dump = f"{level_str}ReqIFSpecHierarchy(\n"
        dump += f"{level_str}  level: {self.level}\n"
        dump += f"{level_str}  identifier: {self.identifier}\n"
        dump += f"{level_str}  spec_object: {self.spec_object}\n"
        if self.children is not None:
            for child in self.children:
                dump += f"{child.auto_dump()}"
        dump += f"{level_str})\n"
        return dump

    def calculate_base_level(self) -> int:
        assert self.level > 0, f"{self.level}"
        return 12 + (self.level - 1) * 4
