from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


def get_id(value: Any) -> int:
    # benedict instances are wrappers created on the fly around the same
    # underlying dict, so the id of the wrapped dict must be used
    from benedict.dicts.base import BaseDict

    if isinstance(value, BaseDict) and value._dict is not None:
        return id(value._dict)
    return id(value)


@contextmanager
def visit(value: Any, path_ids: set[int]) -> Iterator[bool]:
    """
    Track value as being visited on the current recursion path.
    Yields False if value is already on the path (self-referential structure),
    in this case the caller must not recurse into it again.
    """
    value_id = get_id(value)
    if value_id in path_ids:
        yield False
        return
    path_ids.add(value_id)
    try:
        yield True
    finally:
        path_ids.discard(value_id)
