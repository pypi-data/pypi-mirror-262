from typing import Awaitable, Callable, List, Optional

from ...punish import Punish
from ...typing import Comment

TypeCommentsFilter = Callable[[List[Comment]], Awaitable[Optional[List[Punish]]]]

_filters: List[TypeCommentsFilter] = []

_append_filter_hook = None


def append_filter(new_filter: TypeCommentsFilter) -> TypeCommentsFilter:
    _append_filter_hook()
    _filters.append(new_filter)
    return new_filter
