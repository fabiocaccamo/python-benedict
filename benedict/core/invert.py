# -*- coding: utf-8 -*-


def invert(d, flat=False):
    new_dict = d.copy()
    new_dict.clear()
    for key, value in d.items():
        if flat:
            new_dict.setdefault(value, key)
        else:
            new_dict.setdefault(value, []).append(key)
    return new_dict
