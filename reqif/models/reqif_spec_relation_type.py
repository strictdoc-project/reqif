from typing import Optional


class ReqIFSpecRelationType:
    def __init__(
        self,
        identifier: str,
        last_change: Optional[str],
        long_name: str,
    ):
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: str = long_name
