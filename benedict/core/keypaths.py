from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from benedict.core.keylists import keylists
from benedict.utils import type_util


def keypaths(
    d: Mapping[Any, Any],
    separator: str | None = ".",
    indexes: bool = False,
    sort: bool = True,
) -> list[str]:
    separator = separator or "."
    if not type_util.is_string(separator):
        raise ValueError("separator argument must be a (non-empty) string.")
    kls = keylists(d, indexes=indexes)
    kps = [separator.join([f"{key}" for key in kl]) for kl in kls]
    if sort:
        kps.sort()
    return kps
