from collections.abc import MutableMapping
from typing import Any, TypeVar

from benedict.core.move import move

_K = TypeVar("_K")


def rename(d: MutableMapping[_K, Any], key: _K, key_new: _K) -> None:
    move(d, key, key_new, overwrite=False)
