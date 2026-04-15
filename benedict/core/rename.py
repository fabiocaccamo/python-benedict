from collections.abc import MutableMapping
from typing import Any, TypeVar

from benedict.core.move import move
from benedict.utils import type_util

_K = TypeVar("_K")


def _rename_deep(d: MutableMapping[_K, Any], key: _K, key_new: _K) -> None:
    if key in d:
        move(d, key, key_new, overwrite=False)
    for value in list(d.values()):
        if type_util.is_dict(value):
            _rename_deep(value, key, key_new)
        elif type_util.is_list_or_tuple(value):
            for item in value:
                if type_util.is_dict(item):
                    _rename_deep(item, key, key_new)


def rename(
    d: MutableMapping[_K, Any], key: _K, key_new: _K, deep: bool = False
) -> None:
    if deep:
        # Apply at top level first; for benedict instances this resolves keypaths.
        if key in d:
            move(d, key, key_new, overwrite=False)
        # Then recurse into nested plain dicts (keys are matched literally).
        for value in list(d.values()):
            if type_util.is_dict(value):
                _rename_deep(value, key, key_new)
            elif type_util.is_list_or_tuple(value):
                for item in value:
                    if type_util.is_dict(item):
                        _rename_deep(item, key, key_new)
    else:
        move(d, key, key_new, overwrite=False)
