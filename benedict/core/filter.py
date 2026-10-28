from collections.abc import Callable, MutableMapping
from typing import Any, TypeVar, cast

from benedict.core.clone import clone
from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def _filter_deep_value(value: Any, predicate: Callable[[_K, _V], bool]) -> Any:
    if type_util.is_dict(value):
        return _filter_deep(value, predicate)
    if type_util.is_list_or_tuple(value):
        # Reuse deepcopy's reconstruction protocol to preserve sequence subclasses
        # (including named tuples), while substituting the filtered children.
        memo = {id(item): _filter_deep_value(item, predicate) for item in value}
        return clone(value, memo=memo)
    return value


def _filter_deep(
    d: MutableMapping[_K, _V], predicate: Callable[[_K, _V], bool]
) -> MutableMapping[_K, _V]:
    new_dict = clone(d, empty=True)
    for key in list(d.keys()):
        value = d[key]
        if predicate(key, value):
            new_dict[key] = cast("_V", _filter_deep_value(value, predicate))
    return new_dict


def filter(
    d: MutableMapping[_K, _V],
    predicate: Callable[[_K, _V], bool],
    deep: bool = False,
) -> MutableMapping[_K, _V]:
    if not callable(predicate):
        raise ValueError("predicate argument must be a callable.")
    if deep:
        return _filter_deep(d, predicate)
    new_dict = clone(d, empty=True)
    for key in list(d.keys()):
        value = d[key]
        if predicate(key, value):
            new_dict[key] = value
    return new_dict
