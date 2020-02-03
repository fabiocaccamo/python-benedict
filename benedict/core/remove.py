# -*- coding: utf-8 -*-

from benedict.utils import type_util


def remove(d, keys, *args):
    if type_util.is_string(keys):
        keys = [keys]
    keys += args
    for key in keys:
        d.pop(key, None)
