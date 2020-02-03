# -*- coding: utf-8 -*-


def _items_sorted_by_item_at_index(d, index, reverse):
    return sorted(d.items(), key=lambda item: item[index], reverse=reverse)


def items_sorted_by_keys(d, reverse=False):
    return _items_sorted_by_item_at_index(d, 0, reverse)


def items_sorted_by_values(d, reverse=False):
    return _items_sorted_by_item_at_index(d, 1, reverse)
