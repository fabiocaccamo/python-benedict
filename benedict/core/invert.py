from benedict.core.clone import clone
from benedict.utils import type_util


def _invert_item(d, key, value, flat: bool) -> None:
    if flat:
        d.setdefault(value, key)
    else:
        d.setdefault(value, []).append(key)


def _invert_list(d, key, value, flat: bool) -> None:
    for value_item in value:
        _invert_item(d, key, value_item, flat)


def invert(d, flat: bool = False):
    new_dict = clone(d, empty=True)
    for key, value in d.items():
        if type_util.is_list_or_tuple(value):
            _invert_list(new_dict, key, value, flat)
        else:
            _invert_item(new_dict, key, value, flat)
    return new_dict
