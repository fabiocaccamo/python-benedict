from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from benedict.utils import type_util


def _get_keylist_for_dict(
    d: Mapping[Any, Any], parent_keys: list[Any], indexes: bool
) -> list[list[Any]]:
    keylist = []
    for key, value in d.items():
        keys = parent_keys + [key]
        keylist += [keys]
        keylist += _get_keylist_for_value(value, keys, indexes)
    return keylist


def _get_keylist_for_list(
    ls: Sequence[Any], parent_keys: list[Any], indexes: bool
) -> list[list[Any]]:
    keylist = []
    for key, value in enumerate(ls):
        keys = list(parent_keys)
        keys[-1] += f"[{key}]"
        keylist += [keys]
        keylist += _get_keylist_for_value(value, keys, indexes)
    return keylist


def _get_keylist_for_value(
    value: Mapping[Any, Any] | Sequence[Any], parent_keys: list[Any], indexes: bool
) -> list[list[Any]]:
    if type_util.is_dict(value):
        return _get_keylist_for_dict(value, parent_keys, indexes)
    elif type_util.is_list(value) and indexes:
        return _get_keylist_for_list(value, parent_keys, indexes)
    return []


def keylists(
    d: Mapping[Any, Any] | Sequence[Any], indexes: bool = False
) -> list[list[Any]]:
    return _get_keylist_for_value(d, [], indexes)
