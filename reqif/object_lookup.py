from typing import Dict, List

from reqif.models.reqif_spec_object import ReqIFSpecObject


class ReqIFObjectLookup:
    def __init__(
        self,
        spec_objects_lookup: Dict[str, ReqIFSpecObject],
        spec_relations_parent_lookup: Dict[str, List[str]],
    ):
        self.spec_objects_lookup = spec_objects_lookup
        self.spec_relations_parent_lookup = spec_relations_parent_lookup

    @staticmethod
    def empty():
        return ReqIFObjectLookup(
            spec_objects_lookup={}, spec_relations_parent_lookup={}
        )

    def get_spec_object_by_ref(self, ref) -> ReqIFSpecObject:
        return self.spec_objects_lookup[ref]

    def get_spec_object_parents(self, ref) -> List:
        return self.spec_relations_parent_lookup[ref]
