from typing import Any, Dict, List

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_object import ReqIFSpecObject


@auto_described
class ReqIFObjectLookup:
    def __init__(
        self,
        data_types_lookup: Dict[str, Any],
        spec_types_lookup: Dict,
        spec_objects_lookup: Dict[str, ReqIFSpecObject],
        spec_relations_parent_lookup: Dict[str, List[str]],
    ):
        self.data_types_lookup: Dict[str, Any] = data_types_lookup
        self.spec_types_lookup: Dict = spec_types_lookup
        self.spec_objects_lookup = spec_objects_lookup
        self.spec_relations_parent_lookup = spec_relations_parent_lookup

    @staticmethod
    def empty():
        return ReqIFObjectLookup(
            data_types_lookup={},
            spec_types_lookup={},
            spec_objects_lookup={},
            spec_relations_parent_lookup={},
        )

    def spec_object_exists(self, ref) -> bool:
        return ref in self.spec_objects_lookup

    def get_data_type_by_ref(self, ref) -> Any:
        return self.data_types_lookup[ref]

    def get_spec_type_by_ref(self, ref) -> Any:
        return self.spec_types_lookup[ref]

    def get_spec_object_by_ref(self, ref) -> ReqIFSpecObject:
        return self.spec_objects_lookup[ref]

    def get_spec_object_parents(self, ref) -> List:
        return self.spec_relations_parent_lookup[ref]
