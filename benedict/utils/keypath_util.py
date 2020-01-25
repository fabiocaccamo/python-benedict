# -*- coding: utf-8 -*-

from benedict.utils import dict_util

from six import string_types


def check_keys(d, separator):
    """
    Check if dict keys contain keypath separator.
    """
    if not isinstance(d, dict) or not separator:
        return

    def check_key(parent, key, value):
        if key and isinstance(key, string_types) and separator in key:
            raise ValueError(
                'keys should not contain keypath separator '
                '\'{}\', found: \'{}\'.'.format(separator, key))
    dict_util.traverse(d, check_key)


def list_keys(keypath, separator):
    """
    List keys splitting a keypath using the given separator.
    """
    if isinstance(keypath, string_types):
        if separator:
            return keypath.split(separator)
    elif isinstance(keypath, (list, tuple, )):
        keys = []
        for key in keypath:
            keys += list_keys(key, separator)
        return keys
    return [keypath]
