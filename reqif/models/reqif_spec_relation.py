from typing import Any, List, Optional

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
        values: Optional[List[SpecObjectAttribute]] = None,
        values_attribute: Optional[SpecObjectAttribute] = None,
        alternative_id: Optional[str] = None,
    ):
        if values is not None and values_attribute is not None:
            raise ValueError(
                "ReqIFSpecRelation: pass either values or the deprecated "
                "values_attribute, not both."
            )
        self.identifier: str = identifier
        self.alternative_id: Optional[str] = alternative_id
        self.relation_type_ref: str = relation_type_ref
        self.source: str = source
        self.target: str = target

        self.xml_node: Optional[Any] = xml_node
        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name

        # A SPEC-RELATION may carry any number of attribute values under
        # <VALUES>, exactly like a SPEC-OBJECT.
        self.values: Optional[List[SpecObjectAttribute]] = values
        if values_attribute is not None:
            self.values = [values_attribute]

    @property
    def values_attribute(self) -> Optional[SpecObjectAttribute]:
        """Deprecated: the first attribute value, or None.

        SPEC-RELATION used to be modelled as carrying at most one attribute
        value. Use .values instead — this discards every value after the first.
        """
        if self.values is None or len(self.values) == 0:
            return None
        return self.values[0]

    @values_attribute.setter
    def values_attribute(self, value: Optional[SpecObjectAttribute]) -> None:
        """Deprecated: replaces all attribute values with a single one."""
        self.values = None if value is None else [value]
