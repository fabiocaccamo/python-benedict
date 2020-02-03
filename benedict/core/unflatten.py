# -*- coding: utf-8 -*-

from benedict.dicts.keylist import keylist_util
from benedict.utils import type_util


def unflatten(d, separator='_'):
    new_dict = d.copy()
    new_dict.clear()
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        new_value = unflatten(
            value, separator=separator) if type_util.is_dict(value) else value
        new_keys = key.split(separator)
        keylist_util.set_item(new_dict, new_keys, new_value)
    return new_dict
