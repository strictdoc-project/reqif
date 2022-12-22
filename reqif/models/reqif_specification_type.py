from typing import List, Dict, Optional

from reqif.helpers.debug import auto_str
from reqif.models.reqif_spec_object_type import SpecAttributeDefinition


class ReqIFSpecificationType:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        description: Optional[str],
        identifier: str,
        last_change: str,
        long_name: str,
        spec_attributes: Optional[List[SpecAttributeDefinition]],
        spec_attribute_map: Dict[str, str],
    ):
        self.description: Optional[str] = description
        self.identifier: str = identifier
        self.last_change: str = last_change
        self.long_name: str = long_name
        self.spec_attributes: Optional[
            List[SpecAttributeDefinition]
        ] = spec_attributes
        self.spec_attribute_map = spec_attribute_map

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
