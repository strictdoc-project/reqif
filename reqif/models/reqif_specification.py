from typing import List

from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)


class ReqIFSpecification:
    def __init__(
        self,
        identifier: str,
        long_name: str,
        specification_type: str,
        children: List[ReqIFSpecHierarchy],
    ):
        self.identifier: str = identifier
        self.long_name: str = long_name
        self.specification_type: str = specification_type
        self.children: List[ReqIFSpecHierarchy] = children

    def __str__(self) -> str:
        return (
            f"ReqIFSpecification("
            f"identifier: {self.identifier},"
            f"children: {self.children},"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
