from collections.abc import Callable
from typing import Any

from benedict.core.clone import clone


def filter(d: Any, predicate: Callable[[Any, Any], bool]) -> Any:
    if not callable(predicate):
        raise ValueError("predicate argument must be a callable.")
    new_dict = clone(d, empty=True)
    keys = list(d.keys())
    for key in keys:
        value = d.get(key)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict
