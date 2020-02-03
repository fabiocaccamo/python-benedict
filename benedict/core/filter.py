# -*- coding: utf-8 -*-


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
