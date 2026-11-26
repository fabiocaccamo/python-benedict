from collections.abc import MutableMapping, Sequence
from typing import Any, TypeVar

from benedict.core.clone import clone
from benedict.utils import type_util

_K = TypeVar("_K")
_V = TypeVar("_V")


def _invert_item(d: MutableMapping[Any, Any], key: _K, value: _V, flat: bool) -> None:
    if flat:
        d.setdefault(value, key)
    else:
        d.setdefault(value, []).append(key)


def _invert_list(
    d: MutableMapping[Any, Any], key: _K, value: Sequence[Any], flat: bool
) -> None:
    for value_item in value:
        _invert_item(d, key, value_item, flat)


def invert(d: MutableMapping[_K, _V], flat: bool = False) -> MutableMapping[Any, Any]:
    # Imported here to avoid a circular import at module load time.
    from benedict.dicts.keypath import keypath_util

    # Collect the inverted pairs in a plain dict first: the values become the
    # keys of the result, so they must be handled as literal keys instead of
    # keypaths (issue #671). Otherwise a value like "one.two" would silently
    # create a nested mapping and overwrite unrelated groups.
    inverted: dict[Any, Any] = {}
    for key, value in d.items():
        if type_util.is_list_or_tuple(value):
            _invert_list(inverted, key, value, flat)
        else:
            _invert_item(inverted, key, value, flat)

    new_dict = clone(d, empty=True)
    separator = getattr(new_dict, "_keypath_separator", None)
    for key, value in inverted.items():
        # Values that would be reinterpreted as keypaths cannot be represented
        # as literal keys in a keypath-aware dict, so reject them explicitly.
        if (
            separator
            and type_util.is_string(key)
            and keypath_util.parse_keys(key, separator) != [key]
        ):
            raise ValueError(
                f"invert() cannot use {key!r} as a key because it would be "
                f"interpreted as a keypath, not a literal key."
            )
        new_dict[key] = value

    return new_dict
