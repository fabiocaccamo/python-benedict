from __future__ import annotations

import re


def compile_wildcard_pattern(pattern: str) -> re.Pattern[str]:
    """
    Compile a string pattern where * matches any sequence of characters
    and all other characters are matched literally.
    The whole string must match (use regex.match).
    """
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
    # anchor to the absolute end so the whole string must match
    return re.compile(regex + r"\Z", flags=re.DOTALL)
