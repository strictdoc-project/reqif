from typing import List, Optional


class ReqIFSpecHierarchy:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        spec_object: str,
        children: Optional[List],
        ref_then_children_order: bool,
        level: int,
    ):
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

    def __str__(self) -> str:
        return (
            f"ReqIFSpecHierarchy("
            f"identifier: {self.identifier}"
            f", "
            f"last_change: {self.last_change}"
            f", "
            f"long_name: {self.long_name}"
            f", "
            f"level: {self.level}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def calculate_base_level(self) -> int:
        assert self.level > 0, f"{self.level}"
        return 12 + (self.level - 1) * 4
