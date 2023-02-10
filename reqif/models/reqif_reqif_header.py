from typing import Optional

from reqif.helpers.debug import auto_described


@auto_described
class ReqIFReqIFHeader:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: Optional[str] = None,
        comment: Optional[str] = None,
        creation_time: Optional[str] = None,
        repository_id: Optional[str] = None,
        req_if_tool_id: Optional[str] = None,
        req_if_version: Optional[str] = None,
        source_tool_id: Optional[str] = None,
        title: Optional[str] = None,
    ):
        self.identifier: Optional[str] = identifier
        self.comment: Optional[str] = comment
        self.creation_time: Optional[str] = creation_time
        self.repository_id: Optional[str] = repository_id
        self.req_if_tool_id: Optional[str] = req_if_tool_id
        self.req_if_version: Optional[str] = req_if_version
        self.source_tool_id: Optional[str] = source_tool_id
        self.title: Optional[str] = title
