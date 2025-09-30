from __future__ import annotations

from collections.abc import Mapping, MutableSequence, Sequence
from typing import Any, TypeVar

from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V", bound=MutableSequence[Any])


def groupby(items: Sequence[Mapping[_K, Any]], key: _K) -> dict[Any, Any]:
    if not type_util.is_list(items):
        raise ValueError("items should be a list of dicts.")
    items_grouped: dict[Any, Any] = {}
    for item in items:
        if not type_util.is_dict(item):
            raise ValueError("item should be a dict.")
        group = item.get(key)
        if group not in items_grouped:
            items_grouped[group] = []
        items_grouped[group].append(item.copy())
    return items_grouped
