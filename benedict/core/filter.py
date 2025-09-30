from collections.abc import Callable, MutableMapping
from typing import TypeVar

from benedict.core.clone import clone

_K = TypeVar("_K")
_V = TypeVar("_V")


def filter(
    d: MutableMapping[_K, _V], predicate: Callable[[_K, _V], bool]
) -> MutableMapping[_K, _V]:
    if not callable(predicate):
        raise ValueError("predicate argument must be a callable.")
    new_dict = clone(d, empty=True)
    keys = list(d.keys())
    for key in keys:
        value = d[key]
        if predicate(key, value):
            new_dict[key] = value
    return new_dict
