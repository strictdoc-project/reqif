from typing import Dict, List, Optional

from reqif.models.reqif_types import SpecObjectAttributeType


class SpecObjectAttribute:
    def __init__(
        self,
        attribute_type: SpecObjectAttributeType,
        name: str,
        value: str,
        enum_values_then_definition_order: Optional[bool],
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.name: str = name
        self.value: str = value
        self.enum_values_then_definition_order: Optional[
            bool
        ] = enum_values_then_definition_order


class ReqIFSpecObject:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        spec_object_type,
        attributes: List[SpecObjectAttribute],
        attribute_map: Dict[str, SpecObjectAttribute],
        values_then_type_order: bool,
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.spec_object_type = spec_object_type
        self.attributes: List[SpecObjectAttribute] = attributes
        self.attribute_map: Dict[str, SpecObjectAttribute] = attribute_map
        self.values_then_type_order = values_then_type_order

    def __str__(self) -> str:
        return (
            f"ReqIFSpecObject("
            f"description: {self.description}"
            ", "
            f"identifier: {self.identifier}"
            ", "
            f"spec_object_type: {self.spec_object_type}"
            ", "
            f"attributes: {self.attributes}"
            ", "
            f"attribute_map: {self.attribute_map}"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
