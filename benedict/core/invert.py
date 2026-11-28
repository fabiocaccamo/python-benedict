from collections.abc import MutableMapping, Sequence
from typing import Any, TypeVar

from benedict.core.clone import clone
from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def _invert_item(d: MutableMapping[Any, Any], key: _K, value: _V, flat: bool) -> None:
    if flat:
        d.setdefault(value, key)
    else:
        d.setdefault(value, []).append(key)


def _invert_list(
    d: MutableMapping[Any, Any], key: _K, value: Sequence[Any], flat: bool
) -> None:
    for value_item in value:
        _invert_item(d, key, value_item, flat)


def invert(d: MutableMapping[_K, _V], flat: bool = False) -> MutableMapping[Any, Any]:
    # collect items in a plain dict, values used as keys (eg. "a[0]")
    # must not be parsed as keypaths by benedict instances
    items: MutableMapping[Any, Any] = {}
    for key, value in d.items():
        if type_util.is_list_or_tuple(value):
            _invert_list(items, key, value, flat)
        else:
            _invert_item(items, key, value, flat)
    new_dict = clone(d, empty=True)
    new_dict.update(items)
    return new_dict
