from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import TypeVar

_K = TypeVar("_K")
_V = TypeVar("_V")


def find(
    d: Mapping[_K, _V], keys: Iterable[_K], default: _V | None = None
) -> _V | None:
    for key in keys:
        if key in d:
            return d[key]
    return default
