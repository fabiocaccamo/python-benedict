from collections.abc import MutableMapping
from typing import Any, TypeVar, cast

from benedict.core.clone import clone
from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def subset(d: MutableMapping[_K, _V], keys: _K | list[_K], *args: Any) -> Any:
    new_dict = clone(d, empty=True)
    if type_util.is_string(keys):
        keys = [cast("_K", keys)]
    keys += args  # type: ignore[operator]
    for key in cast("list[_K]", keys):
        new_dict[key] = d.get(key)  # type: ignore[assignment]
    return new_dict
