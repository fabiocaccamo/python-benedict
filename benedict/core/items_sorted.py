# -*- coding: utf-8 -*-


def _items_sorted_by(d, key, reverse=False):
    return sorted(d.items(), key=key, reverse=reverse)


def items_sorted_by_keys(d, reverse=False):
    return _items_sorted_by(d, key=lambda item: item[0], reverse=reverse)


def items_sorted_by_values(d, reverse=False):
    return _items_sorted_by(d, key=lambda item: item[1], reverse=reverse)
