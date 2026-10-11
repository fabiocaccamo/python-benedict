from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from benedict.core.keypaths import keypaths
from benedict.utils import pattern_util, type_util


def match(
    d: Mapping[Any, Any],
    pattern: str | re.Pattern[str],
    separator: str | None = ".",
    indexes: bool = True,
) -> list[Any]:
    if type_util.is_regex(pattern):
        regex = pattern
    elif type_util.is_string(pattern):
        regex = pattern_util.compile_wildcard_pattern(pattern)
    else:
        raise ValueError(f"Expected regex or string, found: {type(pattern)}")
    kps = keypaths(d, separator=separator, indexes=indexes)
    values = [d.get(kp) for kp in kps if regex.match(kp)]
    return values
