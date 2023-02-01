from typing import Any

from benedict.utils import type_util


def _merge_dict(d, other, overwrite: bool = True, concat: bool = False) -> None:
    for key, value in other.items():
        _merge_item(d, key, value, overwrite=overwrite, concat=concat)


def _merge_item(d, key, value, overwrite: bool = True, concat: bool = False) -> None:
    if key in d:
        item = d.get(key, None)
        if type_util.is_dict(item) and type_util.is_dict(value):
            _merge_dict(item, value, overwrite=overwrite, concat=concat)
        elif concat and type_util.is_list(item) and type_util.is_list(value):
            item += value
        elif overwrite:
            d[key] = value
    else:
        d[key] = value


def merge(d, other, *args, **kwargs: Any):
    overwrite = kwargs.get("overwrite", True)
    concat = kwargs.get("concat", False)
    others = [other] + list(args)
    for other in others:
        _merge_dict(d, other, overwrite=overwrite, concat=concat)
    return d
