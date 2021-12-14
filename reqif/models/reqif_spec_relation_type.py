class ReqIFSpecRelationType:
    def __init__(
        self,
        identifier: str,
        last_change: str,
        long_name: str,
    ):
        self.identifier: str = identifier
        self.last_change: str = last_change
        self.long_name: str = long_name
