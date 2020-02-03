# -*- coding: utf-8 -*-

from benedict.utils import type_util


def flatten(d, separator='_', **kwargs):
    new_dict = d.copy()
    new_dict.clear()
    keys = list(d.keys())
    base_key = kwargs.pop('base_key', '')
    for key in keys:
        new_key = '{}{}{}'.format(
            base_key, separator, key) if base_key and separator else key
        value = d.get(key, None)
        if type_util.is_dict(value):
            new_value = flatten(value, separator=separator, base_key=new_key)
            new_value.update(new_dict)
            new_dict.update(new_value)
        else:
            new_dict[new_key] = value
    return new_dict
