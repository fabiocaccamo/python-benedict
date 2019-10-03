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
    new_dict = {}
    keys = sorted(d.keys())
    for key in keys:
        value = d.get(key)
        keypath = '{}{}{}'.format(base, separator, key) if base and separator else key
        if isinstance(value, dict):
            new_dict.update(flatten(value, separator, keypath))
        else:
            new_dict[keypath] = value
    return new_dict


def filter(d, predicate):
    if not callable(predicate):
        raise ValueError('predicate argument must be a callable.')
    new_dict = {}
    keys = d.keys()
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict


def invert(d, flat=False):
    if flat:
        new_dict = { value:key for key, value in d.items() }
    else:
        new_dict = {}
        for key, value in d.items():
            new_dict.setdefault(value, []).append(key)
    return new_dict


def items_sorted_by_keys(d, reverse=False):
    return sorted(d.items(), key=lambda item: item[0], reverse=reverse)


def items_sorted_by_values(d, reverse=False):
    return sorted(d.items(), key=lambda item: item[1], reverse=reverse)


def merge(d, other):
    for key, value in other.copy().items():
        src = d.get(key, None)
        if isinstance(src, dict) and isinstance(value, dict):
            merge(src, value)
        else:
            d[key] = value
    return d
