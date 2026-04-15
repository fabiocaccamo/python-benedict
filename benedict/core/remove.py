from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any

from benedict.utils import type_util


def _remove_deep(d: MutableMapping[Any, Any], keys_list: list[Any]) -> None:
    for key in keys_list:
        d.pop(key, None)
    for value in list(d.values()):
        if type_util.is_dict(value):
            _remove_deep(value, keys_list)
        elif type_util.is_list_or_tuple(value):
            for item in value:
                if type_util.is_dict(item):
                    _remove_deep(item, keys_list)


def remove(
    d: MutableMapping[Any, Any], keys: Any, *args: Any, deep: bool = False
) -> None:
    if type_util.is_string(keys):
        keys = [keys]
    keys_list: list[Any] = list(keys) + list(args)
    if deep:
        # Apply at top level first; for benedict instances this resolves keypaths.
        for key in keys_list:
            d.pop(key, None)
        # Then recurse into nested plain dicts (keys are matched literally).
        for value in list(d.values()):
            if type_util.is_dict(value):
                _remove_deep(value, keys_list)
            elif type_util.is_list_or_tuple(value):
                for item in value:
                    if type_util.is_dict(item):
                        _remove_deep(item, keys_list)
    else:
        for key in keys_list:
            d.pop(key, None)
