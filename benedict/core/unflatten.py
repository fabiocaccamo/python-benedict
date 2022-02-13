# -*- coding: utf-8 -*-

from benedict.core import clone
from benedict.dicts.keylist import keylist_util
from benedict.utils import type_util


def _unflatten_item(key, value, separator):
    keys = key.split(separator)
    if type_util.is_dict(value):
        return (keys, unflatten(value, separator=separator))
    return (keys, value)


def unflatten(d, separator="_"):
    new_dict = clone(d, empty=True)
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        new_keys, new_value = _unflatten_item(key, value, separator)
        keylist_util.set_item(new_dict, new_keys, new_value)
    return new_dict
