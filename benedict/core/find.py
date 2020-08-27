# -*- coding: utf-8 -*-


def find(d, keys, default=None):
    for key in keys:
        if key in d:
            return d.get(key, default)
    return default
