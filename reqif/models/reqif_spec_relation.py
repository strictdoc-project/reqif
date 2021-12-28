from typing import Optional


class ReqIFSpecRelation:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        type_then_source_order: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        relation_type_ref,
        source: str,
        target: str,
    ):
        self.type_then_source_order: bool = type_then_source_order
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.relation_type_ref = relation_type_ref
        self.source: str = source
        self.target: str = target
