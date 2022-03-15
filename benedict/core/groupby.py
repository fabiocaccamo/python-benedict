# -*- coding: utf-8 -*-

from benedict.utils import type_util


def groupby(items, key):
    if not type_util.is_list(items):
        raise ValueError("items should be a list of dicts.")
    items_grouped = {}
    for item in items:
        if not type_util.is_dict(item):
            raise ValueError("item should be a dict.")
        group = item.get(key)
        if group not in items_grouped:
            items_grouped[group] = []
        items_grouped[group].append(item.copy())
    return items_grouped
