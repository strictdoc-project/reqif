from typing import Dict, List, Optional

from reqif.helpers.debug import auto_described


@auto_described
class ReqIFDataTypeDefinitionString:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        max_length: Optional[str] = None,
        is_self_closed: bool = True,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.max_length: Optional[str] = max_length
        self.is_self_closed: bool = is_self_closed

    @staticmethod
    def create(
        identifier: str,
    ) -> "ReqIFDataTypeDefinitionString":
        return ReqIFDataTypeDefinitionString(
            identifier=identifier,
        )


@auto_described
class ReqIFDataTypeDefinitionBoolean:
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

    @staticmethod
    def create(
        identifier: str,
    ) -> "ReqIFDataTypeDefinitionBoolean":
        return ReqIFDataTypeDefinitionBoolean(
            identifier=identifier,
        )


@auto_described
class ReqIFDataTypeDefinitionInteger:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        max_value: Optional[str] = None,
        min_value: Optional[str] = None,
        is_self_closed: bool = True,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.max_value: Optional[str] = max_value
        self.min_value: Optional[str] = min_value
        self.is_self_closed: bool = is_self_closed


@auto_described
class ReqIFDataTypeDefinitionReal:  # pylint: disable=too-many-instance-attributes  # noqa: E501
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        accuracy: Optional[int] = None,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        max_value: Optional[str] = None,
        min_value: Optional[str] = None,
        is_self_closed: bool = False,
    ):
        self.identifier: str = identifier
        self.accuracy: Optional[int] = accuracy
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.max_value: Optional[str] = max_value
        self.min_value: Optional[str] = min_value
        self.is_self_closed: bool = is_self_closed


@auto_described
class ReqIFEnumValue:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        key: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        other_content: Optional[str] = None,
        long_name: Optional[str] = None,
    ):
        self.identifier: str = identifier
        self.key: str = key
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.other_content: Optional[str] = other_content
        self.long_name: Optional[str] = long_name

    @staticmethod
    def create(identifier: str, key: str):
        return ReqIFEnumValue(
            identifier=identifier,
            key=key,
        )


@auto_described
class ReqIFDataTypeDefinitionEnumeration:  # pylint: disable=too-many-instance-attributes # noqa: E501
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        multi_valued: Optional[bool] = None,
        values: Optional[List[ReqIFEnumValue]] = None,
        is_self_closed: bool = False,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.multi_valued: Optional[bool] = multi_valued
        self.values: Optional[List[ReqIFEnumValue]] = values
        self.values_map: Dict[str, ReqIFEnumValue] = {}
        if values is not None:
            for value in values:
                self.values_map[value.identifier] = value
        self.is_self_closed: bool = is_self_closed

    @staticmethod
    def create(identifier: str, values: Optional[List[ReqIFEnumValue]]):
        return ReqIFDataTypeDefinitionEnumeration(
            identifier=identifier,
            values=values,
        )


@auto_described
class ReqIFDataTypeDefinitionXHTML:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        is_self_closed: bool = False,
    ):
        self.identifier: str = identifier
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.is_self_closed: bool = is_self_closed


@auto_described
class ReqIFDataTypeDefinitionDateIdentifier:
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
