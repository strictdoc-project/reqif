from typing import Optional, List, Union

from reqif.helpers.debug import auto_described
from reqif.models.reqif_spec_object import ReqIFSpecObject
from reqif.models.reqif_spec_object_type import ReqIFSpecObjectType
from reqif.models.reqif_spec_relation import ReqIFSpecRelation
from reqif.models.reqif_spec_relation_type import ReqIFSpecRelationType
from reqif.models.reqif_specification import ReqIFSpecification
from reqif.models.reqif_specification_type import ReqIFSpecificationType


@auto_described
class ReqIFReqIFContent:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        data_types: Optional[List],
        spec_types: Optional[
            List[
                Union[
                    ReqIFSpecObjectType,
                    ReqIFSpecRelationType,
                    ReqIFSpecificationType,
                ]
            ]
        ],
        spec_objects: Optional[List[ReqIFSpecObject]],
        spec_relations: Optional[List[ReqIFSpecRelation]],
        specifications: Optional[List[ReqIFSpecification]],
        spec_relation_groups: Optional[List],
    ):
        self.data_types: Optional[List] = data_types
        self.spec_types: Optional[
            List[
                Union[
                    ReqIFSpecObjectType,
                    ReqIFSpecRelationType,
                    ReqIFSpecificationType,
                ]
            ]
        ] = spec_types
        self.spec_objects: Optional[List[ReqIFSpecObject]] = spec_objects
        self.spec_relations: Optional[List[ReqIFSpecRelation]] = spec_relations
        self.specifications: Optional[List[ReqIFSpecification]] = specifications
        self.spec_relation_groups: Optional[List] = spec_relation_groups
