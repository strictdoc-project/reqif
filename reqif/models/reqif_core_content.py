from typing import Optional

from reqif.helpers.debug import auto_described
from reqif.models.reqif_req_if_content import ReqIFReqIFContent


@auto_described
class ReqIFCoreContent:
    def __init__(self, req_if_content: Optional[ReqIFReqIFContent]):
        self.req_if_content: Optional[ReqIFReqIFContent] = req_if_content
