from typing import Optional, List, Dict

from reqif.helpers.debug import auto_str


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

    @staticmethod
    def create(
        identifier: str,
    ) -> "ReqIFDataTypeDefinitionString":
        return ReqIFDataTypeDefinitionString(
            is_self_closed=True,
            description=None,
            identifier=identifier,
            last_change=None,
            long_name=None,
            max_length=None,
        )


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


class ReqIFDataTypeDefinitionReal:  # pylint: disable=too-many-instance-attributes  # noqa: E501
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        accuracy: Optional[int],
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        max_value: Optional[float],
        min_value: Optional[float],
    ):
        self.is_self_closed: bool = is_self_closed
        self.accuracy: Optional[int] = accuracy
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.max_value: Optional[float] = max_value
        self.min_value: Optional[float] = min_value


class ReqIFEnumValue:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        key: str,
        other_content: Optional[str],
        long_name: Optional[str],
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.key: str = key
        self.other_content: Optional[str] = other_content
        self.long_name: Optional[str] = long_name

    @staticmethod
    def create(identifier: str, key: str):
        return ReqIFEnumValue(
            description=None,
            identifier=identifier,
            last_change=None,
            key=key,
            other_content=None,
            long_name=None,
        )


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
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.multi_valued: Optional[bool] = multi_valued
        self.values: Optional[List[ReqIFEnumValue]] = values
        self.values_map: Dict[str, str] = {}
        if values is not None:
            for value in values:
                self.values_map[value.identifier] = value.key

    @staticmethod
    def create(identifier: str, values: Optional[List[ReqIFEnumValue]]):
        return ReqIFDataTypeDefinitionEnumeration(
            is_self_closed=False,
            description=None,
            identifier=identifier,
            last_change=None,
            long_name=None,
            multi_valued=False,
            values=values,
        )


class ReqIFDataTypeDefinitionXHTML:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name


class ReqIFDataTypeDefinitionDateIdentifier:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        is_self_closed: bool,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
    ):
        self.is_self_closed: bool = is_self_closed
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name

    def __repr__(self):
        return auto_str(self)

    def __str__(self):
        return self.__repr__()
