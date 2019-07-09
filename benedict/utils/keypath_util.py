# -*- coding: utf-8 -*-

from six import string_types


def all_keys(d):
    keys = []
    for key, val in d.items():
        if key not in keys:
            keys.append(key)
        if isinstance(val, dict):
            keys += all_keys(val)
    return keys


def check_keys(keys, separator):
    if not separator:
        return
    for key in keys:
        if key and isinstance(key, string_types) and separator in key:
            raise ValueError(
                'keys should not contain keypath separator '
                '\'{}\'.'.format(separator))


def join_keys(keys, separator):
    return separator.join(keys)


def split_keys(key, separator):
    if not separator:
        return [key]
    elif isinstance(key, string_types):
        keypath = key
        if separator in keypath:
            keys = list(keypath.split(separator))
            return keys
        else:
            return [key]
    elif isinstance(key, (list, tuple, )):
        keys = []
        for key_item in key:
            keys += split_keys(key_item, separator)
        return keys
    else:
        return [key]
