from typing import Any, Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_object import SpecObjectAttribute


@auto_described
class ReqIFSpecRelation:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        relation_type_ref: str,
        source: str,
        target: str,
        xml_node: Optional[Any] = None,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        values_attribute: Optional[SpecObjectAttribute] = None,
    ):
        self.identifier: str = identifier
        self.relation_type_ref: str = relation_type_ref
        self.source: str = source
        self.target: str = target

        self.xml_node: Optional[Any] = xml_node
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.values_attribute: Optional[SpecObjectAttribute] = values_attribute
