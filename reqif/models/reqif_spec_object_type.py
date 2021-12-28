from typing import List, Optional

from reqif.models.reqif_types import SpecObjectAttributeType


class SpecAttributeDefinition:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        attribute_type: SpecObjectAttributeType,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        datatype_definition: str,
        long_name: Optional[str],
        editable: Optional[bool],
        default_value: Optional[bool],
        multi_valued: Optional[bool],
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.datatype_definition: str = datatype_definition
        self.long_name: Optional[str] = long_name
        self.editable: Optional[bool] = (
            editable == "true" if editable is not None else None
        )
        self.default_value: Optional[bool] = default_value
        self.multi_valued: Optional[bool] = multi_valued

    def __str__(self) -> str:
        return (
            f"SpecAttributeDefinition("
            f"attribute_type={self.attribute_type}"
            ", "
            f"description={self.description}"
            ", "
            f"identifier={self.identifier}"
            ", "
            f"last_change={self.last_change}"
            ", "
            f"datatype_definition={self.datatype_definition}"
            ", "
            f"long_name={self.long_name}"
            ", "
            f"default_value={self.default_value}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ReqIFSpecObjectType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: str,
        long_name,
        attribute_definitions: Optional[List[SpecAttributeDefinition]],
        attribute_map,
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: str = last_change
        self.long_name = long_name
        self.attribute_definitions: Optional[
            List[SpecAttributeDefinition]
        ] = attribute_definitions
        self.attribute_map = attribute_map

    def __str__(self) -> str:
        return (
            f"ReqIFSpecObjectType("
            f"description: {self.description}"
            ", "
            f"identifier: {self.identifier}"
            ", "
            f"attribute_definitions: {self.attribute_definitions}"
            ", "
            f"attribute_map: {self.attribute_map}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
