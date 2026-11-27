from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from benedict.core.keylists import keylist_items
from benedict.utils import type_util


def keypath_items(
    d: Mapping[Any, Any],
    separator: str | None = ".",
    indexes: bool = False,
    sort: bool = True,
) -> list[tuple[str, Any]]:
    """
    Return a list of (keypath, value) pairs for all the keypaths in the dict.
    """
    separator = "." if separator is None else separator
    if not type_util.is_string(separator) or not separator:
        raise ValueError("separator argument must be a (non-empty) string.")
    items = [
        (separator.join([f"{key}" for key in keys]), value)
        for keys, value in keylist_items(d, indexes=indexes)
    ]
    if sort:
        items.sort(key=lambda item: item[0])
    return items


def keypaths(
    d: Mapping[Any, Any],
    separator: str | None = ".",
    indexes: bool = False,
    sort: bool = True,
) -> list[str]:
    items = keypath_items(d, separator=separator, indexes=indexes, sort=sort)
    return [keypath for keypath, _ in items]
