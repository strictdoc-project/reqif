from typing import Optional, List

from reqif.helpers.debug import auto_str
from reqif.models.reqif_spec_object import ReqIFSpecObject
from reqif.models.reqif_spec_object_type import ReqIFSpecObjectType
from reqif.models.reqif_spec_relation import ReqIFSpecRelation
from reqif.models.reqif_specification import ReqIFSpecification


class ReqIFReqIFContent:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        data_types: Optional[List],
        spec_types: Optional[List[ReqIFSpecObjectType]],
        spec_objects: Optional[List[ReqIFSpecObject]],
        spec_relations: Optional[List[ReqIFSpecRelation]],
        specifications: Optional[List[ReqIFSpecification]],
        spec_relation_groups: Optional[List],
    ):
        self.data_types: Optional[List] = data_types
        self.spec_types: Optional[List[ReqIFSpecObjectType]] = spec_types
        self.spec_objects: Optional[List[ReqIFSpecObject]] = spec_objects
        self.spec_relations: Optional[List[ReqIFSpecRelation]] = spec_relations
        self.specifications: Optional[List[ReqIFSpecification]] = specifications
        self.spec_relation_groups: Optional[List] = spec_relation_groups

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
