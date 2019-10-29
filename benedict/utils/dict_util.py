# -*- coding: utf-8 -*-

from six import string_types, text_type
from slugify import slugify

import copy
import json
import re


def clean(d, strings=True, dicts=True, lists=True):
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if not value:
            if value is None or \
                    strings and isinstance(value, string_types) or \
                    dicts and isinstance(value, dict) or \
                    lists and isinstance(value, (list, set, tuple, )):
                del d[key]


def clone(d):
    return copy.deepcopy(d)


def dump(data):
    def encoder(obj):
        json_types = (bool, dict, float, int, list, tuple, ) + string_types
        if not isinstance(obj, json_types):
            return str(obj)
    return json.dumps(data, indent=4, sort_keys=True, default=encoder)


def filter(d, predicate):
    if not callable(predicate):
        raise ValueError('predicate argument must be a callable.')
    new_dict = d.__class__()
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict


def flatten(d, separator='_', base=''):
    new_dict = d.__class__()
    keys = list(d.keys())
    for key in keys:
        keypath = '{}{}{}'.format(
            base, separator, key) if base and separator else key
        value = d.get(key, None)
        if isinstance(value, dict):
            new_value = flatten(value, separator=separator, base=keypath)
            new_value.update(new_dict)
            new_dict.update(new_value)
        else:
            new_dict[keypath] = value
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


def keypaths(d, separator='.'):
    if not separator or not isinstance(separator, string_types):
        raise ValueError('separator argument must be a (non-empty) string.')
    def f(parent, parent_keys):
        kp = []
        for key, value in parent.items():
            keys = parent_keys + [key]
            kp += [separator.join(text_type(k) for k in keys)]
            if isinstance(value, dict):
                kp += f(value, keys)
        return kp
    kp = f(d, [])
    kp.sort()
    return kp


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
    if key_dest == key_src:
        return
    d[key_dest] = d.pop(key_src)


def remove(d, keys, *args):
    if isinstance(keys, string_types):
        keys = [keys]
    keys += args
    for key in keys:
        d.pop(key, None)


def standardize(d):
    def f(parent, key, value):
        if isinstance(key, string_types):
            # https://stackoverflow.com/a/12867228/2096218
            norm_key = re.sub(
                r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', key)
            norm_key = slugify(norm_key, separator='_')
            move(parent, key, norm_key)
    traverse(d, f)


def subset(d, keys, *args):
    new_dict = d.__class__()
    if isinstance(keys, string_types):
        keys = [keys]
    keys += args
    for key in keys:
        new_dict[key] = d.get(key, None)
    return new_dict


def swap(d, key1, key2):
    if key1 == key2:
        return
    d[key1], d[key2] = d[key2], d[key1]


def traverse(d, callback):
    if not callable(callback):
        raise ValueError('callback argument must be a callable.')
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        callback(d, key, value)
        if isinstance(value, dict):
            traverse(value, callback)


def unique(d):
    values = []
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if value in values:
            d.pop(key, None)
            continue
        values.append(value)
