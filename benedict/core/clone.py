# -*- coding: utf-8 -*-

import copy


def clone(obj, empty=False, memo=None):
    d = copy.deepcopy(obj, memo)
    if empty:
        d.clear()
    return d
