from __future__ import annotations

import copy
from collections.abc import MutableMapping
from typing import Any, TypeVar

_T = TypeVar("_T")


def clone(
    obj: _T,
    empty: bool = False,
    memo: dict[int, Any] | None = None,
) -> _T:
    d = copy.deepcopy(obj, memo)
    if empty and isinstance(d, MutableMapping):
        d.clear()
    return d
