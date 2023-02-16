from typing import Any, Dict, List, Optional, Union

from reqif.helpers.debug import auto_described
from reqif.models.reqif_types import SpecObjectAttributeType


@auto_described
class SpecObjectAttribute:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        attribute_type: SpecObjectAttributeType,
        definition_ref: str,
        value: Union[str, List[str]],
        value_stripped_xhtml: Optional[str] = None,
        xml_node: Optional[Any] = None,
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.definition_ref: str = definition_ref
        self.value: Union[str, List[str]] = value
        # Only for XHTML attributes: A value stripped of the
        # <xhtml:...> namespace. <xhtml:div> becomes <div>...
        self.value_stripped_xhtml: Optional[str] = value_stripped_xhtml
        self.xml_node: Optional[Any] = xml_node


@auto_described
class ReqIFSpecObject:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        attributes: List[SpecObjectAttribute],
        spec_object_type: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        xml_node: Optional[Any] = None,
    ):
        self.identifier: str = identifier
        self.attributes: List[SpecObjectAttribute] = attributes
        self.spec_object_type: str = spec_object_type

        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.xml_node: Optional[Any] = xml_node

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
            identifier=identifier,
            spec_object_type=spec_object_type,
            attributes=attributes,
        )
