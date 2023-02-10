from typing import Any, List, Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)
from reqif.models.reqif_spec_object import SpecObjectAttribute


@auto_described
class ReqIFSpecification:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        values: Optional[List[SpecObjectAttribute]] = None,
        specification_type: Optional[str] = None,
        children: Optional[List[ReqIFSpecHierarchy]] = None,
        xml_node: Optional[Any] = None,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.values: Optional[List[SpecObjectAttribute]] = values
        self.specification_type: Optional[str] = specification_type
        self.children: Optional[List[ReqIFSpecHierarchy]] = children
        self.xml_node: Optional[Any] = xml_node
