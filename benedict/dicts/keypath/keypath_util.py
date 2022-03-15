# -*- coding: utf-8 -*-

from benedict.core import traverse
from benedict.utils import type_util

import re


KEY_INDEX_RE = r"(?:\[[\'\"]*(\-?[\d]+)[\'\"]*\]){1}$"


def check_keys(d, separator):
    """
    Check if dict keys contain keypath separator.
    """
    if not type_util.is_dict(d) or not separator:
        return

    def check_key(parent, key, value):
        if key and type_util.is_string(key) and separator in key:
            raise ValueError(
                f"Key should not contain keypath separator '{separator}', found: '{key}'."
            )

    traverse(d, check_key)


def parse_keys(keypath, separator):
    """
    Parse keys from keylist or keypath using the given separator.
    """
    if type_util.is_list_or_tuple(keypath):
        keys = []
        for key in keypath:
            keys += parse_keys(key, separator)
        return keys
    return _split_keys_and_indexes(keypath, separator)


def _split_key_indexes(key):
    """
    Splits key indexes:
    eg. 'item[0][1]' -> ['item', 0, 1].
    """
    if "[" in key and key.endswith("]"):
        keys = []
        while True:
            matches = re.findall(KEY_INDEX_RE, key)
            if matches:
                key = re.sub(KEY_INDEX_RE, "", key)
                index = int(matches[0])
                keys.insert(0, index)
                # keys.insert(0, { keylist_util.INDEX_KEY:index })
                continue
            keys.insert(0, key)
            break
        return keys
    return [key]


def _split_keys(keypath, separator):
    """
    Splits keys using the given separator:
    eg. 'item.subitem[1]' -> ['item', 'subitem[1]'].
    """
    if separator:
        return keypath.split(separator)
    return [keypath]


def _split_keys_and_indexes(keypath, separator):
    """
    Splits keys and indexes using the given separator:
    eg. 'item[0].subitem[1]' -> ['item', 0, 'subitem', 1].
    """
    if type_util.is_string(keypath):
        keys1 = _split_keys(keypath, separator)
        keys2 = []
        for key in keys1:
            keys2 += _split_key_indexes(key)
        return keys2
    return [keypath]
