from typing import Optional


class ReqIFReqIFHeader:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: Optional[str],
        comment: Optional[str],
        creation_time: Optional[str],
        req_if_tool_id: Optional[str],
        req_if_version: Optional[str],
        source_tool_id: Optional[str],
        title: Optional[str],
    ):
        self.identifier: Optional[str] = identifier
        self.comment: Optional[str] = comment
        self.creation_time: Optional[str] = creation_time
        self.req_if_tool_id: Optional[str] = req_if_tool_id
        self.req_if_version: Optional[str] = req_if_version
        self.source_tool_id: Optional[str] = source_tool_id
        self.title: Optional[str] = title
