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
    new_dict = d.__class__()
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
    new_dict = d.__class__()
    keys = d.keys()
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict


def invert(d, flat=False):
    new_dict = d.__class__()
    if flat:
        for key, value in d.items():
            new_dict.setdefault(value, key)
    else:
        for key, value in d.items():
            new_dict.setdefault(value, []).append(key)
    return new_dict


def items_sorted_by_keys(d, reverse=False):
    return sorted(d.items(), key=lambda item: item[0], reverse=reverse)


def items_sorted_by_values(d, reverse=False):
    return sorted(d.items(), key=lambda item: item[1], reverse=reverse)


def merge(d, other, *args):
    others = [other] + list(args)
    for other in others:
        for key, value in other.items():
            src = d.get(key, None)
            if isinstance(src, dict) and isinstance(value, dict):
                merge(src, value)
            else:
                d[key] = value
    return d


def move(d, key_src, key_dest):
    d[key_dest] = d.pop(key_src)


def remove(d, keys, *args):
    if isinstance(keys, string_types):
        keys = [keys]
    keys += args
    for key in keys:
        d.pop(key, None)


def subset(d, keys, *args):
    new_dict = d.__class__()
    if isinstance(keys, string_types):
        keys = [keys]
    keys += args
    for key in keys:
        new_dict[key] = d.get(key, None)
    return new_dict


def swap(d, key1, key2):
    d[key1], d[key2] = d[key2], d[key1]


def unique(d):
    values = []
    keys = sorted(d.keys())
    for key in keys:
        value = d.get(key, None)
        if value in values:
            d.pop(key, None)
            continue
        values.append(value)
