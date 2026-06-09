"""
Optional progress reporting for parsing and unparsing.

ReqIF files coming from real-world tools can contain hundreds of thousands
of spec objects, and parsing or unparsing them takes long enough that
embedding applications need progress feedback. Following the convention of
urllib.request.urlretrieve(reporthook=...), the parse and unparse entry
points accept an optional callback:

    def progress(section: str, items_done: int, items_total: int) -> None

``section`` is the ReqIF container tag being processed (for example,
"SPEC-OBJECTS"), ``items_done`` is the number of the container's direct
children processed so far, and ``items_total`` is the container's total
number of direct children. The callback is invoked once per child, so
callers that display progress should throttle their own output.

When no callback is passed, no callback-related work is done at all.
"""

from typing import Callable, Iterator, Optional, Protocol, TypeVar

ReqIFProgressCallback = Callable[[str, int, int], None]

_T_co = TypeVar("_T_co", covariant=True)


class SizedIterable(Protocol[_T_co]):
    """Anything supporting both len() and iteration, e.g. lists and lxml
    elements."""

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[_T_co]: ...


def track_progress(
    items: "SizedIterable[_T_co]",
    section: str,
    progress: Optional[ReqIFProgressCallback],
) -> Iterator[_T_co]:
    """
    Iterate ``items``, reporting each consumed item to ``progress``.

    With ``progress=None``, this is a plain pass-through iteration.
    """
    if progress is None:
        yield from items
        return
    items_total = len(items)
    for index, item in enumerate(items):
        yield item
        progress(section, index + 1, items_total)
