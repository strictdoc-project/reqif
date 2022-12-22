from typing import Dict, List, Optional, Any

from reqif.helpers.debug import auto_str
from reqif.models.reqif_types import SpecObjectAttributeType


class SpecObjectAttribute:
    def __init__(
        self,
        xml_node: Optional[Any],
        attribute_type: SpecObjectAttributeType,
        definition_ref: str,
        value: str,
    ):
        self.xml_node: Optional[Any] = xml_node
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.definition_ref: str = definition_ref
        self.value: str = value

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)


class ReqIFSpecObject:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        xml_node: Optional[Any],
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        spec_object_type,
        attributes: List[SpecObjectAttribute],
    ):
        self.xml_node: Optional[Any] = xml_node
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.spec_object_type = spec_object_type
        self.attributes: List[SpecObjectAttribute] = attributes
        self.attribute_map: Dict[str, SpecObjectAttribute] = {}
        for attribute in attributes:
            self.attribute_map[attribute.definition_ref] = attribute

    @staticmethod
    def create(
        identifier: str,
        spec_object_type: str,
        attributes: List[SpecObjectAttribute],
    ):
        return ReqIFSpecObject(
            xml_node=None,
            description=None,
            identifier=identifier,
            last_change=None,
            long_name=None,
            spec_object_type=spec_object_type,
            attributes=attributes,
        )

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
