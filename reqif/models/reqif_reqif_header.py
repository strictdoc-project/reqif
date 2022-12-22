from typing import Optional

from reqif.helpers.debug import auto_str


class ReqIFReqIFHeader:  # pylint: disable=too-many-instance-attributes
    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: Optional[str],
        comment: Optional[str],
        creation_time: Optional[str],
        repository_id: Optional[str],
        req_if_tool_id: Optional[str],
        req_if_version: Optional[str],
        source_tool_id: Optional[str],
        title: Optional[str],
    ):
        self.identifier: Optional[str] = identifier
        self.comment: Optional[str] = comment
        self.creation_time: Optional[str] = creation_time
        self.repository_id: Optional[str] = repository_id
        self.req_if_tool_id: Optional[str] = req_if_tool_id
        self.req_if_version: Optional[str] = req_if_version
        self.source_tool_id: Optional[str] = source_tool_id
        self.title: Optional[str] = title

    def __str__(self):
        return auto_str(self)

    def __repr__(self):
        return auto_str(self)
