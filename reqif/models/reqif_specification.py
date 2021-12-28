from typing import List, Optional

from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)


class ReqIFSpecification:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        type_then_children_order: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        values: Optional[List],
        specification_type: Optional[str],
        children: List[ReqIFSpecHierarchy],
    ):
        self.type_then_children_order: bool = type_then_children_order
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.values: Optional[List] = values
        self.specification_type: Optional[str] = specification_type
        self.children: List[ReqIFSpecHierarchy] = children

    def __str__(self) -> str:
        return (
            f"ReqIFSpecification("
            f"identifier: {self.identifier},"
            f"last_change: {self.last_change},"
            f"long_name: {self.long_name},"
            f"values: {self.values},"
            f"children: {self.children},"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
