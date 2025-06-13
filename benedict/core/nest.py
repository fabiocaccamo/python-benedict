from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any

from benedict.core.groupby import groupby


def _nest_items(
    nested_items: MutableMapping[Any, list[Any]],
    item: Any,
    id_key: Any,
    children_key: Any,
) -> None:
    children_items = nested_items.pop(item[id_key], [])
    item[children_key] = children_items
    for child_item in children_items:
        _nest_items(nested_items, child_item, id_key, children_key)


def nest(
    items: Sequence[Mapping[Any, Any]],
    id_key: Any,
    parent_id_key: Any,
    children_key: Any,
) -> list[Any] | None:
    if any(
        [id_key == parent_id_key, id_key == children_key, parent_id_key == children_key]
    ):
        raise ValueError("keys should be different.")
    nested_items = groupby(items, parent_id_key)
    root_items = nested_items.get(None, [])
    for item in root_items:
        _nest_items(nested_items, item, id_key, children_key)
    return nested_items.get(None)
