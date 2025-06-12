from __future__ import annotations

from collections.abc import Mapping

from useful_types import SupportsRichComparisonT


def _items_sorted_by_item_at_index(
    d: Mapping[SupportsRichComparisonT, SupportsRichComparisonT],
    index: int,
    reverse: bool,
) -> list[tuple[SupportsRichComparisonT, SupportsRichComparisonT]]:
    return sorted(d.items(), key=lambda item: item[index], reverse=reverse)


def items_sorted_by_keys(
    d: Mapping[SupportsRichComparisonT, SupportsRichComparisonT], reverse: bool = False
) -> list[tuple[SupportsRichComparisonT, SupportsRichComparisonT]]:
    return _items_sorted_by_item_at_index(d, 0, reverse)


def items_sorted_by_values(
    d: Mapping[SupportsRichComparisonT, SupportsRichComparisonT], reverse: bool = False
) -> list[tuple[SupportsRichComparisonT, SupportsRichComparisonT]]:
    return _items_sorted_by_item_at_index(d, 1, reverse)
