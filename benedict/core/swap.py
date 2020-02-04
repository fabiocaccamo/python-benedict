# -*- coding: utf-8 -*-


def swap(d, key1, key2):
    if key1 == key2:
        return
    d[key1], d[key2] = d[key2], d[key1]
