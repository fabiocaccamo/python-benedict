# -*- coding: utf-8 -*-

from benedict.core import clone


def filter(d, predicate):
    if not callable(predicate):
        raise ValueError("predicate argument must be a callable.")
    new_dict = clone(d, empty=True)
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if predicate(key, value):
            new_dict[key] = value
    return new_dict
