import collections
from typing import Deque, Generator

from reqif.models.reqif_spec_hierarchy import ReqIFSpecHierarchy


class SpecificationIterator:
    @staticmethod
    def iterate_specification(specification) -> Generator:
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
