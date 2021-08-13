# -*- coding: utf-8 -*-

from benedict.core import clone
from benedict.utils import type_util


def _flatten_key(base_key, key, separator):
    if base_key and separator:
        return "{}{}{}".format(base_key, separator, key)
    return key


def _flatten_item(d, base_dict, base_key, separator):
    new_dict = base_dict
    keys = list(d.keys())
    for key in keys:
        new_key = _flatten_key(base_key, key, separator)
        value = d.get(key, None)
        if type_util.is_dict(value):
            new_value = _flatten_item(value, base_dict=new_dict, base_key=new_key, separator=separator)
            new_dict.update(new_value)
            continue
        if new_key in new_dict:
            raise KeyError('Invalid key: "{}", key already in flatten dict.'.format(new_key))
        new_dict[new_key] = value
    return new_dict


def flatten(d, separator="."):
    new_dict = clone(d, empty=True)
    return _flatten_item(d, base_dict=new_dict, base_key="", separator=separator)
