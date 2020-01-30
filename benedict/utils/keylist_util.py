# -*- coding: utf-8 -*-

from six import string_types, integer_types


def _get_index(key):
    if isinstance(key, integer_types):
        return key
    return None


def _get_item_value(item, key):
    if isinstance(item, list):
        index = _get_index(key)
        if index is not None:
            return item[index]
    elif isinstance(item, dict):
        return item[key]
    raise KeyError


def get_item(d, keys):
    items = []
    item = d
    value = None
    for key in keys:
        try:
            value = _get_item_value(item, key)
            if isinstance(item, list):
                index = _get_index(key)
                items.append((item, index, value, ))
            else:
                items.append((item, key, value, ))
            item = value
        except (IndexError, KeyError, ):
            items.append((None, None, None, ))
            break
    if not items:
        items = [(None, None, None, )]
    return items[-1]


def set_item_value(item, key, value):
    index = _get_index(key)
    if index is not None:
        try:
            # overwrite existing index
            item[index] = value
        except IndexError:
            # insert index
            item += ([None] * (index - len(item)))
            item.insert(index, value)
    else:
        item[key] = value


def set_item(d, keys, value):
    item = d
    i = 0
    j = len(keys)
    while i < j:
        key = keys[i]
        if i < (j - 1):
            try:
                subitem = _get_item_value(item, key)
                if not isinstance(subitem, (dict, list, )):
                    raise TypeError
            except (IndexError, KeyError, TypeError, ):
                subkey = keys[i + 1]
                subkey_index = _get_index(subkey)
                if subkey_index is not None:
                    subitem = item[key] = []
                else:
                    subitem = item[key] = {}
            item = subitem
            i += 1
            continue
        set_item_value(item, key, value)
        break

