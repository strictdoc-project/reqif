from typing import Optional

from reqif.models.reqif_req_if_content import ReqIFReqIFContent


class ReqIFCoreContent:
    def __init__(self, req_if_content: Optional[ReqIFReqIFContent]):
        self.req_if_content: Optional[ReqIFReqIFContent] = req_if_content

    def __str__(self) -> str:
        return (
            f"ReqIFCoreContent("
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()
