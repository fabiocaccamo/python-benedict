from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from benedict.core.keypaths import keypaths
from benedict.utils import type_util


def _compile_string_pattern(pattern: str) -> re.Pattern[str]:
    # match all characters literally, except the * wildcard
    head, *parts = re.sub(r"\*+", "*", pattern).split("*")
    regex = re.escape(head)
    if parts:
        *middle, tail = parts
        for index, part in enumerate(middle):
            # emulate an atomic group (as fnmatch.translate does) to match
            # the middle parts without catastrophic backtracking
            group = f"g{index}"
            regex += f"(?=(?P<{group}>.*?{re.escape(part)}))(?P={group})"
        regex += ".*" + re.escape(tail)
    # anchor to the absolute end so the full keypath must be consumed
    return re.compile(regex + r"\Z", flags=re.DOTALL)


def match(
    d: Mapping[Any, Any],
    pattern: str | re.Pattern[str],
    separator: str | None = ".",
    indexes: bool = True,
) -> list[Any]:
    if type_util.is_regex(pattern):
        regex = pattern
    elif type_util.is_string(pattern):
        regex = _compile_string_pattern(pattern)
    else:
        raise ValueError(f"Expected regex or string, found: {type(pattern)}")
    kps = keypaths(d, separator=separator, indexes=indexes)
    values = [d.get(kp) for kp in kps if regex.match(kp)]
    return values
