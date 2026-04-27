from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def _items_sorted_by_item_at_index(
    d: Mapping[Any, Any],
    index: int,
    reverse: bool,
) -> list[tuple[Any, Any]]:
    return sorted(d.items(), key=lambda item: item[index], reverse=reverse)


def items_sorted_by_keys(
    d: Mapping[Any, Any], reverse: bool = False
) -> list[tuple[Any, Any]]:
    return _items_sorted_by_item_at_index(d, 0, reverse)


def items_sorted_by_values(
    d: Mapping[Any, Any], reverse: bool = False
) -> list[tuple[Any, Any]]:
    return _items_sorted_by_item_at_index(d, 1, reverse)
