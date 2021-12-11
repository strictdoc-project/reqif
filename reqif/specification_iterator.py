import collections
from typing import Deque

from reqif.models.reqif_spec_hierarchy import ReqIFSpecHierarchy


class SpecificationIterator:
    @staticmethod
    def iterate_specification(specification):
        task_list: Deque[ReqIFSpecHierarchy] = collections.deque(
            specification.children
        )

        while True:
            if not task_list:
                break
            current = task_list.popleft()

            yield current

            task_list.extendleft(reversed(current.children))
