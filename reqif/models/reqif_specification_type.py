from typing import Dict, List, Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_object_type import SpecAttributeDefinition


@auto_described
class ReqIFSpecificationType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: str,
        long_name: Optional[str],
        spec_attributes: Optional[List[SpecAttributeDefinition]],
        spec_attribute_map: Dict[str, str],
        is_self_closed: bool = False,
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: str = last_change
        self.long_name: Optional[str] = long_name
        self.spec_attributes: Optional[
            List[SpecAttributeDefinition]
        ] = spec_attributes
        self.spec_attribute_map = spec_attribute_map
        self.is_self_closed: bool = is_self_closed
