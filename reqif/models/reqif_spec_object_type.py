from typing import Any, Dict, List, Optional, Union

from reqif.helpers.debug import auto_described
from reqif.models.reqif_types import SpecObjectAttributeType


class DefaultValueEmptySelfClosedTag:
    pass


@auto_described
class SpecAttributeDefinition:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        attribute_type: SpecObjectAttributeType,
        identifier: str,
        datatype_definition: str,
        xml_node: Optional[Any] = None,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        editable: Optional[bool] = None,
        default_value_definition_ref: Optional[str] = None,
        default_value: Union[None, DefaultValueEmptySelfClosedTag, str] = None,
        editable_dedicated_tag: Optional[bool] = None,
        multi_valued: Optional[bool] = None,
    ):
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.identifier: str = identifier
        self.datatype_definition: str = datatype_definition

        self.xml_node: Optional[Any] = xml_node
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.editable: Optional[bool] = (
            editable == "true" if editable is not None else None
        )
        self.default_value_definition_ref: Optional[
            str
        ] = default_value_definition_ref
        self.default_value: Union[
            None, DefaultValueEmptySelfClosedTag, str
        ] = default_value
        self.editable_dedicated_tag: Optional[bool] = (
            editable == "true" if editable is not None else None
        )

        self.multi_valued: Optional[bool] = multi_valued

    @staticmethod
    def create(
        attribute_type: SpecObjectAttributeType,
        identifier: str,
        datatype_definition: str,
        long_name: Optional[str] = None,
        multi_valued: Optional[bool] = None,
    ):
        return SpecAttributeDefinition(
            attribute_type=attribute_type,
            identifier=identifier,
            datatype_definition=datatype_definition,
            long_name=long_name,
            multi_valued=multi_valued,
        )


@auto_described
class ReqIFSpecObjectType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        attribute_definitions: Optional[List[SpecAttributeDefinition]] = None,
    ):
        self.identifier: str = identifier

        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.attribute_definitions: Optional[
            List[SpecAttributeDefinition]
        ] = attribute_definitions

        self.attribute_map: Dict[str, SpecAttributeDefinition] = {}
        if attribute_definitions is not None:
            for attribute_definition in attribute_definitions:
                self.attribute_map[
                    attribute_definition.identifier
                ] = attribute_definition

    @staticmethod
    def create(  # pylint: disable=too-many-arguments
        identifier: str,
        long_name: Optional[str] = None,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        attribute_definitions: Optional[List[SpecAttributeDefinition]] = None,
    ):
        return ReqIFSpecObjectType(
            identifier=identifier,
            description=description,
            last_change=last_change,
            long_name=long_name,
            attribute_definitions=attribute_definitions,
        )
