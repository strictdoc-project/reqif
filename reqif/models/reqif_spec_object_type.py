from typing import List, Optional, Union, Any, Dict

from reqif.helpers.debug import auto_str
from reqif.models.reqif_types import SpecObjectAttributeType


class DefaultValueEmptySelfClosedTag:
    pass


class SpecAttributeDefinition:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        xml_node: Optional[Any],
        attribute_type: SpecObjectAttributeType,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        datatype_definition: str,
        long_name: Optional[str],
        editable: Optional[bool],
        default_value: Union[None, DefaultValueEmptySelfClosedTag, str],
        multi_valued: Optional[bool],
    ):
        self.xml_node: Optional[Any] = xml_node
        self.attribute_type: SpecObjectAttributeType = attribute_type
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.datatype_definition: str = datatype_definition
        self.long_name: Optional[str] = long_name
        self.editable: Optional[bool] = (
            editable == "true" if editable is not None else None
        )
        self.default_value: Union[
            None, DefaultValueEmptySelfClosedTag, str
        ] = default_value
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
            xml_node=None,
            attribute_type=attribute_type,
            description=None,
            identifier=identifier,
            last_change=None,
            datatype_definition=datatype_definition,
            long_name=long_name,
            editable=None,
            default_value=None,
            multi_valued=multi_valued,
        )

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)


class ReqIFSpecObjectType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        long_name: Optional[str],
        attribute_definitions: Optional[List[SpecAttributeDefinition]],
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
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
            description=description,
            identifier=identifier,
            last_change=last_change,
            long_name=long_name,
            attribute_definitions=attribute_definitions,
        )

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
