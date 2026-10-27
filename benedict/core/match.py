from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

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
    separator = "." if separator is None else separator
    if not type_util.is_string(separator) or not separator:
        raise ValueError("separator argument must be a (non-empty) string.")
    items: list[tuple[str, Any]] = []

    def collect(value: Any, path: str) -> None:
        items.append((path, value))
        if isinstance(value, Mapping):
            for key, child in value.items():
                collect(child, f"{path}{separator}{key}")
        elif indexes and type_util.is_list_or_tuple(value):
            for index, child in enumerate(value):
                collect(child, f"{path}[{index}]")

    for key, value in d.items():
        collect(value, str(key))
    items.sort(key=lambda item: item[0])
    return [value for path, value in items if regex.match(path)]
