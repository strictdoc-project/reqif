import collections
from typing import Deque, Dict, Generator, List, Optional

from reqif.helpers.debug import auto_described
from reqif.models.error_handling import ReqIFSchemaError
from reqif.models.reqif_core_content import ReqIFCoreContent
from reqif.models.reqif_namespace_info import ReqIFNamespaceInfo
from reqif.models.reqif_req_if_content import ReqIFReqIFContent
from reqif.models.reqif_reqif_header import ReqIFReqIFHeader
from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)
from reqif.models.reqif_spec_object import (
    ReqIFSpecObject,
)
from reqif.models.reqif_spec_object_type import ReqIFSpecObjectType
from reqif.object_lookup import ReqIFObjectLookup


@auto_described
class ReqIFBundle:  # pylint: disable=too-many-instance-attributes
    @staticmethod
    def create_empty(
        namespace: Optional[str],
        configuration: Optional[str],
    ) -> "ReqIFBundle":
        return ReqIFBundle(
            namespace_info=ReqIFNamespaceInfo.empty(
                namespace=namespace, configuration=configuration
            ),
            req_if_header=None,
            core_content=None,
            tool_extensions_tag_exists=False,
            lookup=ReqIFObjectLookup.empty(),
            exceptions=[],
        )

    def __init__(
        self,
        namespace_info: ReqIFNamespaceInfo,
        req_if_header: Optional[ReqIFReqIFHeader],
        core_content: Optional[ReqIFCoreContent],
        tool_extensions_tag_exists: bool,
        lookup: ReqIFObjectLookup,
        exceptions: List[ReqIFSchemaError],
    ):  # pylint: disable=too-many-arguments
        self.namespace_info: ReqIFNamespaceInfo = namespace_info
        self.req_if_header: Optional[ReqIFReqIFHeader] = req_if_header
        self.core_content: Optional[ReqIFCoreContent] = core_content
        self.tool_extensions_tag_exists = tool_extensions_tag_exists
        self.lookup = lookup
        self.exceptions: List[ReqIFSchemaError] = exceptions

    def iterate_specification_hierarchy(self, specification) -> Generator:
        assert isinstance(self.core_content, ReqIFCoreContent)
        assert isinstance(self.core_content.req_if_content, ReqIFReqIFContent)
        assert isinstance(self.core_content.req_if_content.specifications, list)
        assert specification in self.core_content.req_if_content.specifications

        if specification.children is None:
            return

        task_list: Deque[ReqIFSpecHierarchy] = collections.deque(
            specification.children
        )

        while True:
            if not task_list:
                break
            current = task_list.popleft()

            yield current

            if current.children is not None:
                task_list.extendleft(reversed(current.children))

    def get_spec_object_by_ref(self, ref) -> ReqIFSpecObject:
        return self.lookup.get_spec_object_by_ref(ref)

    def get_spec_object_type_by_ref(
        self,
        ref: str,
    ) -> Optional[ReqIFSpecObjectType]:
        if self.core_content is None:
            return None
        if self.core_content.req_if_content is None:
            return None
        if self.core_content.req_if_content.spec_types is None:
            return None
        for spec_type in self.core_content.req_if_content.spec_types:
            if (
                isinstance(spec_type, ReqIFSpecObjectType)
                and spec_type.identifier == ref
            ):
                return spec_type
        return None

    def get_spec_object_parents(self, ref) -> List:
        return self.lookup.get_spec_object_parents(ref)


@auto_described
class ReqIFZBundle:
    def __init__(
        self,
        reqif_bundles: Dict[str, ReqIFBundle],
        attachments: Dict[str, bytes],
    ):  # pylint: disable=too-many-arguments
        self.reqif_bundles: Dict[str, ReqIFBundle] = reqif_bundles
        self.attachments: Dict[str, bytes] = attachments
