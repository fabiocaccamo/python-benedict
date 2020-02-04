# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _get_keylist(item, parent_keys):
    l = []
    for key, value in item.items():
        keys = parent_keys + [key]
        l += [keys]
        if type_util.is_dict(value):
            l += _get_keylist(value, keys)
    return l


def keylists(d):
    return _get_keylist(d, [])
