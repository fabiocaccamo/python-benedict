from collections.abc import MutableMapping
from typing import Any


def unique(d: MutableMapping[Any, Any]) -> None:
    values = []
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if value in values:
            d.pop(key, None)
            continue
        values.append(value)
