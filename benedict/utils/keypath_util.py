# -*- coding: utf-8 -*-

from six import string_types


def join_keys(keys, separator):
    return separator.join(keys)


def split_keys(key, separator):
    if isinstance(key, string_types):
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

