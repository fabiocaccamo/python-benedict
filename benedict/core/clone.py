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
        # The deep copy carries the frozen flag, which would make clearing it
        # raise. An empty clone is a fresh container for the caller to fill,
        # so it does not inherit the source's frozen state. The copy is used
        # rather than a new instance to keep settings such as the keypath
        # separator.
        unfreeze = getattr(d, "unfreeze", None)
        if callable(unfreeze):
            unfreeze()
        d.clear()
    return d
