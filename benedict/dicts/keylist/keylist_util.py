# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _get_index(key):
    if type_util.is_integer(key):
        return key
    return None


def _get_item_key_and_value(item, key, parent=None):
    if type_util.is_list_or_tuple(item) and type_util.is_wildcard(key):
        return key, item
    elif (
        type_util.is_list_or_tuple(item)
        and type_util.is_wildcard(parent)
        and type_util.contains_only_dict(item)
        and any(key in _item.keys() for _item in item)
    ):
        return key, [_item for _item in item if key in _item.keys()]
    elif type_util.is_list_or_tuple(item):
        index = _get_index(key)
        if index is not None:
            return (index, item[index])
    elif type_util.is_dict(item):
        return (key, item[key])
    raise KeyError(f"Invalid key: '{key}'")


def _get_or_new_item_value(item, key, subkey):
    try:
        _, value = _get_item_key_and_value(item, key)
        if not type_util.is_dict_or_list_or_tuple(value):
            raise TypeError
    except (IndexError, KeyError, TypeError):
        value = _new_item_value(subkey)
        _set_item_value(item, key, value)
    return value


def _new_item_value(key):
    index = _get_index(key)
    return {} if index is None else []


def _set_item_value(item, key, value):
    index = _get_index(key)
    if index is not None:
        try:
            # overwrite existing index
            item[index] = value
        except IndexError:
            # insert index
            item += [None] * (index - len(item))
            item.insert(index, value)
    elif type_util.is_list(item):
        for idx, _item in enumerate(value):
            if _item is not None:
                item[idx].update({key: _item})
    else:
        item[key] = value


def get_item(d, keys):
    items = get_items(d, keys)
    return items[-1] if items else (None, None, None)


def get_items(d, keys):
    items = []
    item = d
    for key in keys:
        try:
            if any(items) and type_util.is_wildcard(val=key):
                parent = items[-1][1]
            elif any(items) and type_util.is_wildcard(items[-1][1]):
                parent = items[-1][1]
            else:
                parent = None
            item_key, item_value = _get_item_key_and_value(item, key, parent)
            items.append((item, item_key, item_value))
            item = item_value
        except (IndexError, KeyError):
            items.append((None, None, None))
            break
    return items


def set_item(d, keys, value):
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
