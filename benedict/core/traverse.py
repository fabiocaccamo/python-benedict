# -*- coding: utf-8 -*-

from benedict.utils import type_util


def _traverse_collection(d, callback):
    if type_util.is_dict(d):
        _traverse_dict(d, callback)
    elif type_util.is_list_or_tuple(d):
        _traverse_list(d, callback)


def _traverse_dict(d, callback):
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        callback(d, key, value)
        _traverse_collection(value, callback)


def _traverse_list(ls, callback):
    items = list(enumerate(ls))
    for index, value in items:
        callback(ls, index, value)
        _traverse_collection(value, callback)


def traverse(d, callback):
    if not callable(callback):
        raise ValueError("callback argument must be a callable.")
    _traverse_collection(d, callback)
