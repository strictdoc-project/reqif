from typing import Dict, List, Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_object_type import SpecAttributeDefinition


@auto_described
class ReqIFSpecificationType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        description: Optional[str] = None,
        last_change: Optional[str] = None,
        long_name: Optional[str] = None,
        spec_attributes: Optional[List[SpecAttributeDefinition]] = None,
        spec_attribute_map: Optional[Dict[str, str]] = None,
        is_self_closed: bool = False,
    ):
        self.identifier: str = identifier

        self.description: Optional[str] = description
        self.last_change: Optional[str] = last_change
        self.long_name: Optional[str] = long_name
        self.spec_attributes: Optional[
            List[SpecAttributeDefinition]
        ] = spec_attributes
        self.spec_attribute_map: Optional[Dict[str, str]] = spec_attribute_map
        self.is_self_closed: bool = is_self_closed
