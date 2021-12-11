from typing import Optional, List

from reqif.models.reqif_spec_object import ReqIFSpecObject


class ReqIFReqIFContent:
    def __init__(self, spec_objects: Optional[List[ReqIFSpecObject]]):
        self.spec_objects: Optional[List[ReqIFSpecObject]] = spec_objects
