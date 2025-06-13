import re
from collections.abc import MutableMapping
from typing import Any

from slugify import slugify

from benedict.core.rename import rename
from benedict.core.traverse import traverse
from benedict.utils import type_util


def _standardize_item(d: MutableMapping[Any, Any], key: Any, value: Any) -> None:
    if type_util.is_string(key):
        # https://stackoverflow.com/a/12867228/2096218
        norm_key = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", key)
        norm_key = slugify(norm_key, separator="_")
        rename(d, key, norm_key)


def standardize(d: MutableMapping[Any, Any]) -> None:
    traverse(d, _standardize_item)  # type: ignore[arg-type]
