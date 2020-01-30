# -*- coding: utf-8 -*-

from benedict.utils import keylist_util, type_util

from slugify import slugify

import copy
import json
import re


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


def clone(d):
    return copy.deepcopy(d)


def dump(data):
    def encoder(obj):
        if not type_util.is_json_serializable(obj):
            return str(obj)
    return json.dumps(data, indent=4, sort_keys=True, default=encoder)


def filter(d, predicate):
    if not callable(predicate):
        raise ValueError('predicate argument must be a callable.')
    new_dict = d.copy()
    new_dict.clear()
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict


def flatten(d, separator='_', **kwargs):
    new_dict = d.copy()
    new_dict.clear()
    keys = list(d.keys())
    base_key = kwargs.pop('base_key', '')
    for key in keys:
        new_key = '{}{}{}'.format(
            base_key, separator, key) if base_key and separator else key
        value = d.get(key, None)
        if type_util.is_dict(value):
            new_value = flatten(value, separator=separator, base_key=new_key)
            new_value.update(new_dict)
            new_dict.update(new_value)
        else:
            new_dict[new_key] = value
    return new_dict


def invert(d, flat=False):
    new_dict = d.copy()
    new_dict.clear()
    for key, value in d.items():
        if flat:
            new_dict.setdefault(value, key)
        else:
            new_dict.setdefault(value, []).append(key)
    return new_dict


def items_sorted_by(d, key, reverse=False):
    return sorted(d.items(), key=key, reverse=reverse)


def items_sorted_by_keys(d, reverse=False):
    return items_sorted_by(d, key=lambda item: item[0], reverse=reverse)


def items_sorted_by_values(d, reverse=False):
    return items_sorted_by(d, key=lambda item: item[1], reverse=reverse)


def keypaths(d, separator='.'):
    if not separator or not type_util.is_string(separator):
        raise ValueError('separator argument must be a (non-empty) string.')

    def f(parent, parent_keys):
        kp = []
        for key, value in parent.items():
            keys = parent_keys + [key]
            kp += [separator.join('{}'.format(k) for k in keys)]
            if type_util.is_dict(value):
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
            if type_util.is_dict(src) and type_util.is_dict(value):
                merge(src, value)
            else:
                d[key] = value
    return d


def move(d, key_src, key_dest, overwrite=True):
    if key_dest == key_src:
        return
    if key_dest in d and not overwrite:
        raise KeyError
    d[key_dest] = d.pop(key_src)


def remove(d, keys, *args):
    if type_util.is_string(keys):
        keys = [keys]
    keys += args
    for key in keys:
        d.pop(key, None)


def rename(d, key, key_new):
    move(d, key, key_new, overwrite=False)


def search(d, query,
           in_keys=True, in_values=True, exact=False, case_sensitive=True):
    items = []

    def get_term(value):
        v_is_str = type_util.is_string(value)
        v = value.lower() if (v_is_str and not case_sensitive) else value
        return (v, v_is_str, )

    q, q_is_str = get_term(query)

    def get_match(cond, value):
        if not cond:
            return False
        v, v_is_str = get_term(value)
        # TODO: add regex support
        if exact:
            return q == v
        elif q_is_str and v_is_str:
            return q in v
        return False

    def search_item(item_dict, item_key, item_value):
        if get_match(in_keys, item_key) or get_match(in_values, item_value):
            items.append((item_dict, item_key, item_value, ))
    traverse(d, search_item)
    return items


def standardize(d):
    def standardize_item(item_dict, item_key, item_value):
        if type_util.is_string(item_key):
            # https://stackoverflow.com/a/12867228/2096218
            norm_key = re.sub(
                r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', item_key)
            norm_key = slugify(norm_key, separator='_')
            rename(item_dict, item_key, norm_key)
    traverse(d, standardize_item)


def subset(d, keys, *args):
    new_dict = d.copy()
    new_dict.clear()
    if type_util.is_string(keys):
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
        if type_util.is_dict(value):
            traverse(value, callback)


def unflatten(d, separator='_'):
    new_dict = d.copy()
    new_dict.clear()
    new_dict_cursor = new_dict
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        new_value = unflatten(
            value, separator=separator) if type_util.is_dict(value) else value
        new_keys = key.split(separator)
        keylist_util.set_item(new_dict, new_keys, new_value)
    return new_dict


def unique(d):
    values = []
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if value in values:
            d.pop(key, None)
            continue
        values.append(value)
