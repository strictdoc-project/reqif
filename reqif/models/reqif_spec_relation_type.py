from typing import Optional


class ReqIFSpecRelationType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: str,
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: str = long_name
