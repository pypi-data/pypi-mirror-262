from typing import Awaitable, Callable, List, Optional

from ...punish import Punish
from ...typing import Thread

TypeThreadsFilter = Callable[[List[Thread]], Awaitable[Optional[List[Punish]]]]

_filters: List[TypeThreadsFilter] = []

_append_filter_hook = None


def append_filter(new_filter: TypeThreadsFilter) -> TypeThreadsFilter:
    _append_filter_hook()
    _filters.append(new_filter)
    return new_filter
