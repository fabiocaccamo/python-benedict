# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _get_keylist(item, parent_keys):
    keylist = []
    for key, value in item.items():
        keys = parent_keys + [key]
        keylist += [keys]
        if type_util.is_dict(value):
            keylist += _get_keylist(value, keys)
    return keylist


def keylists(d):
    return _get_keylist(d, [])
