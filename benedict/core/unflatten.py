from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

from benedict.core.clone import clone
from benedict.dicts.keylist import keylist_util
from benedict.utils import type_util


def _unflatten_item(key: str, value: Any, separator: str) -> tuple[list[Any], Any]:
    keys = key.split(separator)
    if type_util.is_dict(value):
        return (keys, unflatten(value, separator=separator))
    return (keys, value)


def unflatten(d: MutableMapping[Any, Any], separator: str = "_") -> Any:
    new_dict = clone(d, empty=True)
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        new_keys, new_value = _unflatten_item(key, value, separator)
        keylist_util.set_item(new_dict, new_keys, new_value)
    return new_dict
