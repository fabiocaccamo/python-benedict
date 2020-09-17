# -*- coding: utf-8 -*-

from benedict.core import clone
from benedict.utils import type_util


def subset(d, keys, *args):
    new_dict = clone(d, empty=True)
    if type_util.is_string(keys):
        keys = [keys]
    keys += args
    for key in keys:
        new_dict[key] = d.get(key, None)
    return new_dict
