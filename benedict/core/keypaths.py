# -*- coding: utf-8 -*-

from benedict.core.keylists import keylists
from benedict.utils import type_util


def keypaths(d, separator='.'):
    if not separator or not type_util.is_string(separator):
        raise ValueError('separator argument must be a (non-empty) string.')

    kls = keylists(d)
    kps = [separator.join(['{}'.format(key) for key in kl]) for kl in kls]
    kps.sort()
    return kps
