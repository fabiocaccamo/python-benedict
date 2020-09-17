# -*- coding: utf-8 -*-

import copy


def clone(obj, empty=False):
    d = copy.deepcopy(obj)
    if empty:
        d.clear()
    return d
