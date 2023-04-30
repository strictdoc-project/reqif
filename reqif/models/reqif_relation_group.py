from typing import List, Optional


class ReqIFRelationGroup:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        type_ref: Optional[str] = None,
        source_specification_ref: Optional[str] = None,
        target_specification_ref: Optional[str] = None,
        spec_relations: Optional[List[str]] = None,
        is_self_closed: bool = True,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.type_ref: Optional[str] = type_ref
        self.source_specification_ref: Optional[str] = source_specification_ref
        self.target_specification_ref: Optional[str] = target_specification_ref
        self.spec_relations: Optional[List[str]] = spec_relations
        self.is_self_closed: bool = is_self_closed
