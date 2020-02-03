# -*- coding: utf-8 -*-

from benedict.utils import type_util


def merge(d, other, *args):
    others = [other] + list(args)
    for other in others:
        for key, value in other.items():
            src = d.get(key, None)
            if type_util.is_dict(src) and type_util.is_dict(value):
                merge(src, value)
            else:
                d[key] = value
    return d
