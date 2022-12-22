from typing import Optional, Any

from reqif.helpers.debug import auto_str
from reqif.models.reqif_spec_object import SpecObjectAttribute


class ReqIFSpecRelation:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        xml_node: Optional[Any],
        description: Optional[str],
        identifier: str,
        last_change: Optional[str],
        relation_type_ref,
        source: str,
        target: str,
        values_attribute: Optional[SpecObjectAttribute],
    ):
        self.xml_node: Optional[Any] = xml_node
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: Optional[str] = last_change
        self.relation_type_ref = relation_type_ref
        self.source: str = source
        self.target: str = target
        self.values_attribute: Optional[SpecObjectAttribute] = values_attribute

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
