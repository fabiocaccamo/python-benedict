# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _merge_dict(d, other, overwrite=True):
    for key, value in other.items():
        _merge_item(d, key, value, overwrite)


def _merge_item(d, key, value, overwrite=True):
    if key in d:
        item = d.get(key, None)
        if type_util.is_dict(item) and type_util.is_dict(value):
            _merge_dict(item, value, overwrite)
        elif overwrite:
            d[key] = value
    else:
        d[key] = value


def merge(d, other, *args, **kwargs):
    overwrite = kwargs.get('overwrite', True)
    others = [other] + list(args)
    for other in others:
        _merge_dict(d, other, overwrite)
    return d
