from collections.abc import MutableMapping
from typing import Any, TypeVar

_K = TypeVar("_K")


def swap(d: MutableMapping[_K, Any], key1: _K, key2: _K) -> None:
    if key1 == key2:
        return
    val1 = d[key1]
    val1 = val1.copy() if isinstance(val1, dict) else val1
    val2 = d[key2]
    val2 = val2.copy() if isinstance(val2, dict) else val2
    d[key1], d[key2] = val2, val1
