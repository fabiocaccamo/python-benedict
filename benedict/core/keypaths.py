# -*- coding: utf-8 -*-

from benedict.utils import type_util


def keypaths(d, separator='.'):
    if not separator or not type_util.is_string(separator):
        raise ValueError('separator argument must be a (non-empty) string.')

    def f(parent, parent_keys):
        kp = []
        for key, value in parent.items():
            keys = parent_keys + [key]
            kp += [separator.join('{}'.format(k) for k in keys)]
            if type_util.is_dict(value):
                kp += f(value, keys)
        return kp
    kp = f(d, [])
    kp.sort()
    return kp
