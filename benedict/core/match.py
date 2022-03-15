# -*- coding: utf-8 -*-

from benedict.core.keypaths import keypaths
from benedict.utils import type_util

import re


def match(d, pattern, separator=".", indexes=True):
    if type_util.is_regex(pattern):
        regex = pattern
    elif type_util.is_string(pattern):
        # all indexes wildcard support
        pattern = re.sub(r"([\*]{1})", "(.)*", pattern)
        # escape square brackets
        pattern = re.sub(r"(\[([^\[\]]*)\])", "\\[\\g<2>\\]", pattern)
        regex = re.compile(pattern, flags=re.DOTALL)
    else:
        raise ValueError(f"Expected regex or string, found: {type(pattern)}")
    kps = keypaths(d, separator=separator, indexes=indexes)
    values = [d.get(kp) for kp in kps if regex.match(kp)]
    return values
