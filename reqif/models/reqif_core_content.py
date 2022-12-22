from typing import Optional

from reqif.helpers.debug import auto_str
from reqif.models.reqif_req_if_content import ReqIFReqIFContent


class ReqIFCoreContent:
    def __init__(self, req_if_content: Optional[ReqIFReqIFContent]):
        self.req_if_content: Optional[ReqIFReqIFContent] = req_if_content

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
