from __future__ import annotations

from collections.abc import MutableMapping, MutableSequence
from typing import Any, TypeVar

_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")


def _clean_dict(
    d: MutableMapping[_K, _V], strings: bool, collections: bool
) -> MutableMapping[_K, _V]:
    keys = list(d.keys())
    for key in keys:
        d[key] = _clean_value(d[key], strings=strings, collections=collections)
        if d[key] is None:
            del d[key]
    return d


def _clean_list(
    ls: MutableSequence[_T], strings: bool, collections: bool
) -> MutableSequence[_T]:
    for i in range(len(ls) - 1, -1, -1):
        ls[i] = _clean_value(ls[i], strings=strings, collections=collections)
        if ls[i] is None:
            ls.pop(i)
    return ls


def _clean_set(values: set[_T], strings: bool, collections: bool) -> set[_T]:
    return {
        value
        for value in values
        if _clean_value(value, strings=strings, collections=collections) is not None
    }


def _clean_str(s: str, strings: bool, collections: bool) -> str | None:
    return s if s and s.strip() else None


def _clean_tuple(
    values: tuple[_T, ...], strings: bool, collections: bool
) -> tuple[_T, ...]:
    return tuple(
        value
        for value in values
        if _clean_value(value, strings=strings, collections=collections) is not None
    )


def _clean_value(value: Any, strings: bool, collections: bool) -> Any:
    if value is None:
        return value
    elif isinstance(value, MutableSequence) and collections:
        value = _clean_list(value, strings=strings, collections=collections) or None
    elif isinstance(value, MutableMapping) and collections:
        value = (
            _clean_dict(dict(value), strings=strings, collections=collections) or None
        )
    elif isinstance(value, set) and collections:
        value = _clean_set(value, strings=strings, collections=collections) or None
    elif isinstance(value, str) and strings:
        value = _clean_str(value, strings=strings, collections=collections) or None
    elif isinstance(value, tuple) and collections:
        value = _clean_tuple(value, strings=strings, collections=collections) or None
    return value


def clean(d: Any, strings: bool = True, collections: bool = True) -> Any:
    return _clean_dict(d, strings=strings, collections=collections)
