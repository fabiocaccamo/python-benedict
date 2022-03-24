# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _get_keylist_for_dict(d, parent_keys, indexes):
    keylist = []
    for key, value in d.items():
        keys = parent_keys + [key]
        keylist += [keys]
        keylist += _get_keylist_for_value(value, keys, indexes)
    return keylist


def _get_keylist_for_list(ls, parent_keys, indexes):
    keylist = []
    for key, value in enumerate(ls):
        keys = list(parent_keys)
        keys[-1] += f"[{key}]"
        keylist += [keys]
        keylist += _get_keylist_for_value(value, keys, indexes)
    return keylist


def _get_keylist_for_value(value, parent_keys, indexes):
    if type_util.is_dict(value):
        return _get_keylist_for_dict(value, parent_keys, indexes)
    elif type_util.is_list(value) and indexes:
        return _get_keylist_for_list(value, parent_keys, indexes)
    return []


def keylists(d, indexes=False):
    return _get_keylist_for_value(d, [], indexes)
