from typing import Dict, List, Optional

from reqif.models.reqif_types import SpecObjectAttributeType


class SpecObjectAttribute:
    def __init__(
        self, attribute_type: SpecObjectAttributeType, name: str, value: str
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.name: str = name
        self.value: str = value


class ReqIFSpecObject:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        last_change: Optional[str],
        spec_object_type,
        attributes: List[SpecObjectAttribute],
        attribute_map: Dict[str, SpecObjectAttribute],
    ):
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.spec_object_type = spec_object_type
        self.attributes: List[SpecObjectAttribute] = attributes
        self.attribute_map: Dict[str, SpecObjectAttribute] = attribute_map

    def __str__(self) -> str:
        return (
            f"ReqIFSpecObject("
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
