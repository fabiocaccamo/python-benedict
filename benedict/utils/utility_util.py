# -*- coding: utf-8 -*-

from six import string_types

import copy
import json


def clean(d, strings=True, dicts=True, lists=True):
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if not value:
            if value is None or \
                    strings and isinstance(value, string_types) or \
                    dicts and isinstance(value, dict) or \
                    lists and isinstance(value, (list, tuple, )):
                del d[key]


def clone(d):
    return copy.deepcopy(d)


def dump(data):
    def encoder(obj):
        json_types = (bool, dict, float, int, list, tuple, ) + string_types
        if not isinstance(obj, json_types):
            return str(obj)
    return json.dumps(data, indent=4, sort_keys=True, default=encoder)


def flatten(d, separator='_', base=''):
    f = {}
    keys = sorted(d.keys())
    for key in keys:
        value = d.get(key)
        keypath = '{}{}{}'.format(base, separator, key) if base and separator else key
        if isinstance(value, dict):
            f.update(flatten(value, separator, keypath))
        else:
            f[keypath] = value
    return f


def filter(d, predicate):
    f = {}
    keys = d.keys()
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            f[key] = value
    return f


def merge(d, other):
    for key, value in other.copy().items():
        src = d.get(key, None)
        if isinstance(src, dict) and isinstance(value, dict):
            merge(src, value)
        else:
            d[key] = value
    return d
