# -*- coding: utf-8 -*-

from benedict.utils import type_util


def subset(d, keys, *args):
    new_dict = d.copy()
    new_dict.clear()
    if type_util.is_string(keys):
        keys = [keys]
    keys += args
    for key in keys:
        new_dict[key] = d.get(key, None)
    return new_dict
