from typing import List, Optional

from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)
from reqif.models.reqif_spec_object import SpecObjectAttribute


class ReqIFSpecification:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        xml_node,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        values: Optional[List[SpecObjectAttribute]],
        specification_type: Optional[str],
        children: Optional[List[ReqIFSpecHierarchy]],
    ):
        self.xml_node = xml_node
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.values: Optional[List[SpecObjectAttribute]] = values
        self.specification_type: Optional[str] = specification_type
        self.children: Optional[List[ReqIFSpecHierarchy]] = children

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
