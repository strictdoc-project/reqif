from typing import List, Optional

from reqif.models.reqif_types import SpecObjectAttributeType


class SpecAttributeDefinition:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        attribute_type: SpecObjectAttributeType,
        identifier: str,
        last_change: Optional[str],
        datatype_definition: str,
        long_name: str,
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.datatype_definition: str = datatype_definition
        self.long_name: str = long_name

    def __str__(self) -> str:
        return (
            f"SpecAttributeDefinition("
            f"attribute_type={self.attribute_type}"
            ", "
            f"identifier={self.identifier}"
            ", "
            f"last_change={self.last_change}"
            ", "
            f"datatype_definition={self.datatype_definition}"
            ", "
            f"long_name={self.long_name}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ReqIFSpecObjectType:
    def __init__(
        self,
        identifier,
        long_name,
        attribute_definitions: List[SpecAttributeDefinition],
        attribute_map,
    ):
        self.identifier = identifier
        self.long_name = long_name
        self.attribute_definitions: List[
            SpecAttributeDefinition
        ] = attribute_definitions
        self.attribute_map = attribute_map

    def __str__(self) -> str:
        return (
            f"ReqIFSpecObjectType("
            f"identifier: {self.identifier}"
            ", "
            f"attribute_definitions: {self.attribute_definitions}"
            ", "
            f"attribute_map: {self.attribute_map}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
