from __future__ import annotations

from collections.abc import MutableMapping
from typing import Any, TypeVar

from benedict.core.clone import clone
from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def subset(
    d: MutableMapping[_K, _V], keys: _K | list[_K], *args: Any
) -> MutableMapping[_K, _V | None]:
    new_dict: MutableMapping[_K, _V | None] = clone(d, empty=True)  # type: ignore[arg-type]
    if type_util.is_string(keys):
        key_list: list[_K] = [keys]
    else:
        key_list = list(keys) if isinstance(keys, list) else [keys]
    key_list.extend(args)
    for key in key_list:
        new_dict[key] = d.get(key)
    return new_dict
