from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any, TypeVar

from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def _get_index(key: Any) -> int | None:
    if type_util.is_integer(key):
        return key
    return None


def _get_item_key_and_value(item: Any, key: Any) -> tuple[Any, Any]:
    if type_util.is_list_or_tuple(item):
        index = _get_index(key)
        if index is not None:
            return (index, item[index])
    elif type_util.is_dict(item):
        return (key, item[key])
    raise KeyError(f"Invalid key: {key!r}")


def _get_or_new_item_value(item: Any, key: Any, subkey: Any) -> Any:
    try:
        _, value = _get_item_key_and_value(item, key)
        if not type_util.is_dict_or_list_or_tuple(value):
            raise TypeError
    except (IndexError, KeyError, TypeError):
        value = _new_item_value(subkey)
        _set_item_value(item, key, value)
    return value


def _new_item_value(key: Any) -> dict[Any, Any] | list[Any]:
    index = _get_index(key)
    return {} if index is None else []


def _set_item_value(item: Any, key: Any, value: Any) -> None:
    index = _get_index(key)
    if index is not None:
        try:
            # overwrite existing index
            item[index] = value
        except IndexError:
            # insert index
            item += [None] * (index - len(item))
            item.insert(index, value)
    else:
        item[key] = value


def get_item(
    d: Mapping[_K, _V], keys: Sequence[Any]
) -> tuple[Mapping[_K, _V], _K, _V] | tuple[None, None, None]:
    items = get_items(d, keys)
    return items[-1] if items else (None, None, None)


def get_items(
    d: Mapping[_K, _V], keys: Iterable[Any]
) -> list[tuple[Mapping[_K, _V], _K, _V] | tuple[None, None, None]]:
    items: list[tuple[Mapping[_K, _V], _K, _V] | tuple[None, None, None]] = []
    item = d
    for key in keys:
        try:
            item_key, item_value = _get_item_key_and_value(item, key)
            items.append((item, item_key, item_value))
            item = item_value
        except (IndexError, KeyError):
            items.append((None, None, None))
            break
    return items


def set_item(d: Mapping[_K, _V], keys: Sequence[Any], value: _V) -> None:
    item = d
    i = 0
    j = len(keys)
    while i < j:
        key = keys[i]
        if i < (j - 1):
            item = _get_or_new_item_value(item, key, keys[i + 1])
            i += 1
            continue
        _set_item_value(item, key, value)
        break
