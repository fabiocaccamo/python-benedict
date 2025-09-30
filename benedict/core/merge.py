from collections.abc import Mapping, MutableMapping
from typing import Any, TypeVar

from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def _merge_dict(
    d: MutableMapping[_K, _V],
    other: Mapping[_K, _V],
    overwrite: bool = True,
    concat: bool = False,
) -> None:
    for key, value in other.items():
        _merge_item(d, key, value, overwrite=overwrite, concat=concat)


def _merge_item(
    d: MutableMapping[_K, _V],
    key: _K,
    value: _V,
    overwrite: bool = True,
    concat: bool = False,
) -> None:
    if key in d:
        item = d.get(key)
        if type_util.is_dict(item) and type_util.is_dict(value):
            _merge_dict(item, value, overwrite=overwrite, concat=concat)
        elif concat and type_util.is_list(item) and type_util.is_list(value):
            item += value  # type: ignore[assignment]
        elif overwrite:
            d[key] = value
    else:
        d[key] = value


def merge(
    d: MutableMapping[_K, _V], other: Mapping[_K, _V], *args: Any, **kwargs: Any
) -> Any:
    overwrite = kwargs.get("overwrite", True)
    concat = kwargs.get("concat", False)
    others = [other] + list(args)
    for other in others:
        _merge_dict(d, other, overwrite=overwrite, concat=concat)
    return d
