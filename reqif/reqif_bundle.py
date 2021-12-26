import collections
from typing import Dict, List, Deque, Optional

from reqif.models.reqif_core_content import ReqIFCoreContent
from reqif.models.reqif_reqif_header import ReqIFReqIFHeader
from reqif.models.reqif_spec_hierarchy import (
    ReqIFSpecHierarchy,
)
from reqif.models.reqif_spec_object import (
    ReqIFSpecObject,
)
from reqif.models.reqif_spec_relation import (
    ReqIFSpecRelation,
)


class ReqIFBundle:  # pylint: disable=too-many-instance-attributes
    @staticmethod
    def create_empty(
        namespace: Optional[str],
        configuration: Optional[str],
    ) -> "ReqIFBundle":
        return ReqIFBundle(
            namespace=namespace,
            configuration=configuration,
            req_if_header=None,
            core_content=None,
            spec_objects_lookup={},
            spec_relations_parent_lookup={},
            tool_extensions_tag_exists=False,
        )

    def __init__(
        self,
        namespace: Optional[str],
        configuration: Optional[str],
        req_if_header: Optional[ReqIFReqIFHeader],
        core_content: Optional[ReqIFCoreContent],
        spec_objects_lookup: Dict[str, ReqIFSpecObject],
        spec_relations_parent_lookup: Dict[str, List[ReqIFSpecRelation]],
        tool_extensions_tag_exists: bool,
    ):  # pylint: disable=too-many-arguments
        self.namespace: Optional[str] = namespace
        self.configuration: Optional[str] = configuration
        self.req_if_header: Optional[ReqIFReqIFHeader] = req_if_header
        self.core_content: Optional[ReqIFCoreContent] = core_content
        self.spec_objects_lookup = spec_objects_lookup
        self.spec_relations_parent_lookup = spec_relations_parent_lookup
        self.tool_extensions_tag_exists = tool_extensions_tag_exists

    def get_spec_object_by_ref(self, ref) -> ReqIFSpecObject:
        return self.spec_objects_lookup[ref]

    def get_spec_object_parents(self, ref) -> List:
        return self.spec_relations_parent_lookup[ref]

    def iterate_specification_hierarchy(self, specification):
        assert self.core_content
        assert self.core_content.req_if_content
        assert specification in self.core_content.req_if_content.specifications

        task_list: Deque[ReqIFSpecHierarchy] = collections.deque(
            specification.children
        )

        while True:
            if not task_list:
                break
            current = task_list.popleft()

            yield current

            task_list.extendleft(reversed(current.children))
