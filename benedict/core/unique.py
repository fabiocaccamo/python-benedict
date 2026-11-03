from collections.abc import MutableMapping
from typing import Any


def unique(d: MutableMapping[Any, Any]) -> None:
    from benedict.dicts.base import BaseDict

    values = []
    for key, value in list(d.items()):
        if value in values:
            if isinstance(d, BaseDict):
                BaseDict.pop(d, key, None)
            else:
                d.pop(key, None)
            continue
        values.append(value)
