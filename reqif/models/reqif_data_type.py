from typing import Optional


class ReqIFDataTypeDefinitionString:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: str,
        max_length: Optional[str],
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: str = long_name
        self.max_length: Optional[str] = max_length


class ReqIFDataTypeDefinitionInteger:
    def __init__(
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: str,
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: str = long_name


class ReqIFDataTypeDefinitionEnumeration:
    def __init__(self, identifier: str, values_map):
        self.identifier = identifier
        self.values_map = values_map
