from typing import Optional, List


class ReqIFDataTypeDefinitionString:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        max_length: Optional[str],
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
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


class ReqIFEnumValue:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        key: str,
        other_content: Optional[str],
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.key: str = key
        self.other_content: Optional[str] = other_content


class ReqIFDataTypeDefinitionEnumeration:  # pylint: disable=too-many-instance-attributes # noqa:E501
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        multi_valued: Optional[bool],
        values: Optional[List[ReqIFEnumValue]],
        values_map,
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.multi_valued: Optional[bool] = multi_valued
        self.values: Optional[List[ReqIFEnumValue]] = values
        self.values_map = values_map
