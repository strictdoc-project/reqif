from typing import Optional


class ReqIFRelationGroupType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        is_self_closed: bool = True,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.is_self_closed: bool = is_self_closed
