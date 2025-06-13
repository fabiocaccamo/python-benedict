from collections.abc import MutableMapping
from typing import Any, TypeVar

_K = TypeVar("_K")


def move(
    d: MutableMapping[_K, Any], key_src: _K, key_dest: _K, overwrite: bool = True
) -> None:
    if key_dest == key_src:
        return
    if key_dest in d and not overwrite:
        raise KeyError(
            f"Invalid key: {key_dest!r}, key already in "
            "target dict and 'overwrite' is disabled."
        )
    d[key_dest] = d.pop(key_src)
