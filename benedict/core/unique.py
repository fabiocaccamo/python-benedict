# -*- coding: utf-8 -*-


def unique(d):
    values = []
    keys = list(d.keys())
    for key in keys:
        value = d.get(key, None)
        if value in values:
            d.pop(key, None)
            continue
        values.append(value)
