from collections.abc import Mapping
from typing import Any

from benedict.core.clone import clone


def _flatten_key(base_key: str, key: str, separator: str) -> str:
    if base_key and separator:
        return f"{base_key}{separator}{key}"
    return key


def _flatten_item(
    d: Any,
    base_dict: Any,
    base_key: str,
    separator: str,
) -> Any:
    new_dict = base_dict
    keys = list(d.keys())
    for key in keys:
        new_key = _flatten_key(base_key, key, separator)
        value = d.get(key, None)
        if isinstance(value, Mapping):
            new_value = _flatten_item(
                value, base_dict=new_dict, base_key=new_key, separator=separator
            )
            new_dict.update(new_value)
            continue
        if new_key in new_dict:
            raise KeyError(f"Invalid key: {new_key!r}, key already in flatten dict.")
        new_dict[new_key] = value
    return new_dict


def flatten(d: Any, separator: str = "_") -> Any:
    new_dict = clone(d, empty=True)
    return _flatten_item(d, base_dict=new_dict, base_key="", separator=separator)
