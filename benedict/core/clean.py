# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _clean_item(d, key, strings, collections):
    value = d.get(key, None)
    if not value:
        del_none = value is None
        del_string = strings and type_util.is_string(value)
        del_collection = collections and type_util.is_collection(value)
        return any([del_none, del_string, del_collection])

    return False


def clean(d, strings=True, collections=True):
    keys = list(d.keys())
    for key in keys:
        if _clean_item(d, key, strings, collections):
            del d[key]
