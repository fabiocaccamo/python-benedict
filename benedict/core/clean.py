# -*- coding: utf-8 -*-

from benedict.utils import type_util


def clean(d, strings=True, collections=True):
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if not value:
            del_none = value is None
            del_string = strings and type_util.is_string(value)
            del_collection = collections and type_util.is_collection(value)
            if any([del_none, del_string, del_collection]):
                del d[key]
