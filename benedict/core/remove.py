from collections.abc import MutableMapping
from typing import Any

from benedict.utils import type_util


def remove(d: MutableMapping[Any, Any], keys: Any, *args: Any) -> None:
    if type_util.is_string(keys):
        keys = [keys]
    keys += args
    for key in keys:
        d.pop(key, None)
