from __future__ import annotations

from collections.abc import Callable, MutableMapping, Sequence
from typing import Any, TypeVar

from benedict.utils import cycle_util, type_util

_K = TypeVar("_K")
_V = TypeVar("_V")

TraverseCallback = Callable[
    [MutableMapping[_K, _V] | Sequence[Any] | None, _K | int, _V | None], None
]


def _traverse_collection(
    d: MutableMapping[_K, _V] | Sequence[Any] | _V | None,
    callback: TraverseCallback[_K, _V],
    path_ids: set[int],
) -> None:
    if type_util.is_dict(d):
        with cycle_util.visit(d, path_ids) as visiting:
            if visiting:
                _traverse_dict(d, callback, path_ids)
    elif type_util.is_list_or_tuple(d):
        with cycle_util.visit(d, path_ids) as visiting:
            if visiting:
                _traverse_list(d, callback, path_ids)


def _traverse_dict(
    d: MutableMapping[_K, _V],
    callback: TraverseCallback[_K, _V],
    path_ids: set[int],
) -> None:
    keys = list(d.keys())
    for key in keys:
        value = d.get(key)
        callback(d, key, value)
        _traverse_collection(value, callback, path_ids)


def _traverse_list(
    ls: Sequence[Any], callback: TraverseCallback[_K, _V], path_ids: set[int]
) -> None:
    items = list(enumerate(ls))
    for index, value in items:
        callback(ls, index, value)
        _traverse_collection(value, callback, path_ids)


def traverse(d: MutableMapping[_K, _V], callback: TraverseCallback[_K, _V]) -> None:
    if not callable(callback):
        raise ValueError("callback argument must be a callable.")
    _traverse_collection(d, callback, set())
