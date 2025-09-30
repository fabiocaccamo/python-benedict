from __future__ import annotations

import re
from collections.abc import (
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
from typing import (
    Any,
    cast,
)

from typing_extensions import Self, TypeVar

from benedict.core import clean as _clean
from benedict.core import clone as _clone
from benedict.core import dump as _dump
from benedict.core import filter as _filter
from benedict.core import find as _find
from benedict.core import flatten as _flatten
from benedict.core import groupby as _groupby
from benedict.core import invert as _invert
from benedict.core import items_sorted_by_keys as _items_sorted_by_keys
from benedict.core import items_sorted_by_values as _items_sorted_by_values
from benedict.core import keypaths as _keypaths
from benedict.core import match as _match
from benedict.core import merge as _merge
from benedict.core import move as _move
from benedict.core import nest as _nest
from benedict.core import remove as _remove
from benedict.core import rename as _rename
from benedict.core import search as _search
from benedict.core import standardize as _standardize
from benedict.core import subset as _subset
from benedict.core import swap as _swap
from benedict.core import traverse as _traverse
from benedict.core import unflatten as _unflatten
from benedict.core import unique as _unique
from benedict.core.traverse import TraverseCallback
from benedict.dicts.io import IODict
from benedict.dicts.keyattr import KeyattrDict
from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict, keypath_util
from benedict.dicts.parse import ParseDict
from benedict.serializers import JSONSerializer, YAMLSerializer

__all__ = [
    "benedict",
    "IODict",
    "KeyattrDict",
    "KeylistDict",
    "KeypathDict",
    "ParseDict",
]

_KPT = keypath_util.KeyType
_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)


class benedict(KeyattrDict[_K, _V], KeypathDict[_V], IODict[_K, _V], ParseDict[_K, _V]):
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Constructs a new instance.
        """
        if len(args) == 1 and isinstance(args[0], benedict):
            obj = args[0]
            kwargs.setdefault("keyattr_enabled", obj.keyattr_enabled)
            kwargs.setdefault("keyattr_dynamic", obj.keyattr_dynamic)
            kwargs.setdefault("keypath_separator", obj.keypath_separator)
            super().__init__(obj.dict(), **kwargs)
            return
        super().__init__(*args, **kwargs)

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        obj_type = type(self)
        obj = obj_type(
            keyattr_enabled=self._keyattr_enabled,
            keyattr_dynamic=self._keyattr_dynamic,
            keypath_separator=self._keypath_separator,
        )
        for key, value in self.items():
            obj[key] = _clone(value, memo=memo)
        return obj

    def __getitem__(self, key: _KPT) -> Any:  # type: ignore[override]
        return self._cast(super().__getitem__(key))

    def __setitem__(self, key: _KPT, value: _V) -> None:  # type: ignore[override]
        super().__setitem__(key, self._cast(value))

    def _cast(self, value: Any) -> Any:
        """
        Cast a dict instance to a benedict instance
        keeping the pointer to the original dict.
        """
        obj_type = type(self)
        if isinstance(value, Mapping) and not isinstance(value, obj_type):
            return obj_type(
                value,
                keyattr_enabled=self._keyattr_enabled,
                keyattr_dynamic=self._keyattr_dynamic,
                keypath_separator=self._keypath_separator,
                check_keys=False,
            )
        elif isinstance(value, list):
            for index, item in enumerate(value):
                value[index] = self._cast(item)
        return value

    def clean(self, strings: bool = True, collections: bool = True) -> None:
        """
        Clean the current dict instance removing all empty values: None, '', {}, [], ().
        If strings or collections (dict, list, set, tuple) flags are False,
        related empty values will not be deleted.
        """
        _clean(self, strings=strings, collections=collections)

    def clone(self) -> Self:
        """
        Creates and return a clone of the current dict instance (deep copy).
        """
        return cast("Self", self._cast(_clone(self)))

    def copy(self) -> Self:
        """
        Creates and return a copy of the current instance (shallow copy).
        """
        return cast("Self", self._cast(super().copy()))

    def deepcopy(self) -> Self:
        """
        Alias of 'clone' method.
        """
        return self.clone()

    def deepupdate(self, other: Mapping[str, _V], *args: Any) -> None:
        """
        Alias of 'merge' method.
        """
        self.merge(other, *args)

    def dump(self, data: Any = None) -> str:
        """
        Return a readable string representation of any dict/list.
        This method can be used both as static method or instance method.
        """
        return _dump(data or self)

    def filter(self, predicate: Callable[[_KPT, _V], bool]) -> Self:
        """
        Return a new filtered dict using the given predicate function.
        Predicate function receives key, value arguments and should return a bool value.
        """
        return cast("Self", _filter(self, predicate))

    def find(self, keys: Iterable[str], default: _V | None = None) -> _V | None:
        """
        Return the first match searching for the given keys.
        If no result found, default value is returned.
        """
        return _find(self, keys, default)  # type: ignore[misc]

    def flatten(self, separator: str = "_") -> Self:
        """
        Return a new flattened dict using the given separator
        to join nested dict keys to flatten keypaths.
        """
        if separator == self._keypath_separator:
            raise ValueError(
                f"Invalid flatten separator: {separator!r}, "
                "flatten separator must be different from keypath separator."
            )
        return cast("Self", _flatten(self, separator))

    def get(self, key: _KPT, default: _V | None = None) -> Any:  # type: ignore[override]
        return self._cast(super().get(key, default))

    def get_dict(self, key: _K, default: Any = None) -> Any:
        return self._cast(super().get_dict(key, default))

    def get_list_item(
        self, key: _K, index: int = 0, default: Any = None, separator: str = ","
    ) -> Any:
        return self._cast(super().get_list_item(key, index, default, separator))

    def groupby(self, key: _KPT, by_key: _KPT) -> Self:
        """
        Group a list of dicts at key by the value of the given by_key and return a new dict.
        """
        return cast("Self", self._cast(_groupby(self[key], by_key)))

    def invert(self, flat: bool = False) -> Self:
        """
        Return a new inverted dict, where values become keys and keys become values.
        Since multiple keys could have the same value, each value will be a list of keys.
        If flat is True each value will be a single value (use this only if values are unique).
        """
        return cast("Self", _invert(self, flat))

    def items(self) -> Iterator[tuple[_KPT, Any]]:  # type: ignore[override]
        for key, value in super().items():
            yield (key, self._cast(value))  # type: ignore[misc]

    def items_sorted_by_keys(self, reverse: bool = False) -> list[tuple[Any, Any]]:
        """
        Return items (key/value list) sorted by keys.
        If reverse is True, the list will be reversed.
        """
        return _items_sorted_by_keys(self, reverse=reverse)

    def items_sorted_by_values(self, reverse: bool = False) -> list[tuple[Any, Any]]:
        """
        Return items (key/value list) sorted by values.
        If reverse is True, the list will be reversed.
        """
        return _items_sorted_by_values(self, reverse=reverse)

    def keypaths(self, indexes: bool = False, sort: bool = True) -> list[Any]:
        """
        Return a list of all keypaths in the dict.
        If indexes is True, the output will include list values indexes.
        """
        return _keypaths(
            self, separator=self._keypath_separator, indexes=indexes, sort=sort
        )

    def match(self, pattern: str | re.Pattern[str], indexes: bool = True) -> list[Any]:
        """
        Return a list of all values whose keypath
        matches the given pattern (a regex or string).
        If pattern is string, wildcard can be used
        (eg. [*] can be used to match all list indexes).
        If indexes is True, the pattern will be matched also against list values.
        """
        return _match(self, pattern, separator=self._keypath_separator, indexes=indexes)

    def merge(self, other: Mapping[str, _V], *args: Any, **kwargs: Any) -> None:
        """
        Merge one or more dict objects into current instance (deepupdate).
        Sub-dictionaries will be merged together.
        If overwrite is False, existing values will not be overwritten.
        If concat is True, list values will be concatenated together.
        """
        others = [other] + list(args)
        for other in others:
            keypath_util.check_keys(other, self._keypath_separator)
        _merge(self, *others, **kwargs)

    def move(self, key_src: _KPT, key_dest: _KPT) -> None:
        """
        Move a dict instance value item from 'key_src' to 'key_dst'.
        If key_dst exists, its value will be overwritten.
        """
        _move(self, key_src, key_dest)  # type: ignore[misc]

    def nest(
        self,
        key: _KPT,
        id_key: _KPT = "id",
        parent_id_key: _KPT = "parent_id",
        children_key: _KPT = "children",
    ) -> list[Any] | None:
        """
        Nest a list of dicts at the given key and return a new nested list
        using the specified keys to establish the correct items hierarchy.
        """
        return _nest(self[key], id_key, parent_id_key, children_key)

    def pop(self, key: _KPT, *args: Any) -> _V:  # type: ignore[override]
        return cast("_V", self._cast(super().pop(key, *args)))

    def remove(self, keys: Iterable[_KPT], *args: Any) -> None:
        """
        Remove multiple keys from the current dict instance.
        It is possible to pass a single key or more keys (as list or *args).
        """
        _remove(self, keys, *args)

    def setdefault(self, key: _KPT, default: _V | None = None) -> _V:  # type: ignore[override]
        return cast("_V", self._cast(super().setdefault(key, default)))

    def rename(self, key: _KPT, key_new: _KPT) -> None:
        """
        Rename a dict item key from 'key' to 'key_new'.
        If key_new exists, a KeyError will be raised.
        """
        _rename(self, key, key_new)  # type: ignore[misc]

    def search(
        self,
        query: Any,
        in_keys: bool = True,
        in_values: bool = True,
        exact: bool = False,
        case_sensitive: bool = False,
    ) -> list[tuple[dict[str, Any], str, Any]]:
        """
        Search and return a list of items (dict, key, value, ) matching the given query.
        """
        return _search(self, query, in_keys, in_values, exact, case_sensitive)

    def standardize(self) -> None:
        """
        Standardize all dict keys (e.g. 'Location Latitude' -> 'location_latitude').
        """
        _standardize(self)

    def subset(self, keys: Sequence[_KPT], *args: Any) -> Self:
        """
        Return a new dict subset for the given keys.
        It is possible to pass a single key or multiple keys (as list or *args).
        """
        return cast("Self", _subset(self, keys, *args))

    def swap(self, key1: _KPT, key2: _KPT) -> None:
        """
        Swap items values at the given keys.
        """
        _swap(self, key1, key2)  # type: ignore[misc]

    def traverse(self, callback: TraverseCallback[_K, _V]) -> None:
        """
        Traverse the current dict instance (including nested dicts),
        and pass each item (dict, key, value) to the callback function.
        """
        _traverse(self, callback)

    def unflatten(self, separator: str = "_") -> Self:
        """
        Return a new unflattened dict using the given separator
        to split dict keys to nested keypaths.
        """
        return cast("Self", _unflatten(self, separator))

    def unique(self) -> None:
        """
        Remove duplicated values from the current dict instance.
        """
        _unique(self)

    def values(self) -> Iterator[Any]:  # type: ignore[override]
        for value in super().values():
            yield self._cast(value)


# fix benedict json dumps support - #57 #59 #61
JSONSerializer.disable_c_make_encoder()

# fix benedict yaml representer - #43
YAMLSerializer.represent_dict_for_class(benedict)
