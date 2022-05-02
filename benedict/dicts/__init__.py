# -*- coding: utf-8 -*-

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
from benedict.dicts.io import IODict
from benedict.dicts.keylist import KeylistDict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict

# fix benedict json dumps support - #57 #59 #61
from json import encoder

# fix benedict yaml representer - #43
from yaml import SafeDumper
from yaml.representer import SafeRepresenter


__all__ = ["benedict", "IODict", "KeylistDict", "KeypathDict", "ParseDict"]


class benedict(KeypathDict, IODict, ParseDict):
    def __init__(self, *args, **kwargs):
        """
        Constructs a new instance.
        """
        if len(args) == 1 and isinstance(args[0], benedict):
            obj = args[0]
            kwargs.setdefault("keypath_separator", obj.keypath_separator)
            super(benedict, self).__init__(obj.dict(), **kwargs)
            return
        super(benedict, self).__init__(*args, **kwargs)

    def __deepcopy__(self, memo):
        obj = benedict(keypath_separator=self._keypath_separator)
        for key, value in self.items():
            obj[key] = _clone(value, memo=memo)
        return obj

    def __getitem__(self, key):
        return self._cast(super(benedict, self).__getitem__(key))

    def _cast(self, value):
        """
        Cast a dict instance to a benedict instance
        keeping the pointer to the original dict.
        """
        if isinstance(value, dict) and not isinstance(value, benedict):
            return benedict(
                value, keypath_separator=self._keypath_separator, check_keys=False
            )
        return value

    def clean(self, strings=True, collections=True):
        """
        Clean the current dict instance removing all empty values: None, '', {}, [], ().
        If strings or collections (dict, list, set, tuple) flags are False,
        related empty values will not be deleted.
        """
        _clean(self, strings=strings, collections=collections)

    def clone(self):
        """
        Creates and return a clone of the current dict instance (deep copy).
        """
        return self._cast(_clone(self))

    def copy(self):
        """
        Creates and return a copy of the current instance (shallow copy).
        """
        return self._cast(super(benedict, self).copy())

    def deepcopy(self):
        """
        Alias of 'clone' method.
        """
        return self.clone()

    def deepupdate(self, other, *args):
        """
        Alias of 'merge' method.
        """
        self.merge(other, *args)

    def dump(self, data=None):
        """
        Return a readable string representation of any dict/list.
        This method can be used both as static method or instance method.
        """
        return _dump(data or self)

    def filter(self, predicate):
        """
        Return a new filtered dict using the given predicate function.
        Predicate function receives key, value arguments and should return a bool value.
        """
        return _filter(self, predicate)

    def find(self, keys, default=None):
        """
        Return the first match searching for the given keys.
        If no result found, default value is returned.
        """
        return _find(self, keys, default)

    def flatten(self, separator="_"):
        """
        Return a new flattened dict using the given separator
        to join nested dict keys to flatten keypaths.
        """
        if separator == self._keypath_separator:
            raise ValueError(
                f"Invalid flatten separator: '{separator}', "
                "flatten separator must be different from keypath separator."
            )
        return _flatten(self, separator)

    def get(self, key, default=None):
        return self._cast(super(benedict, self).get(key, default))

    def get_dict(self, key, default=None):
        return self._cast(super(benedict, self).get_dict(key, default))

    def get_list_item(self, key, index=0, default=None, separator=","):
        return self._cast(
            super(benedict, self).get_list_item(key, index, default, separator)
        )

    def groupby(self, key, by_key):
        """
        Group a list of dicts at key by the value of the given by_key and return a new dict.
        """
        return self._cast(_groupby(self[key], by_key))

    def invert(self, flat=False):
        """
        Return a new inverted dict, where values become keys and keys become values.
        Since multiple keys could have the same value, each value will be a list of keys.
        If flat is True each value will be a single value (use this only if values are unique).
        """
        return _invert(self, flat)

    def items_sorted_by_keys(self, reverse=False):
        """
        Return items (key/value list) sorted by keys.
        If reverse is True, the list will be reversed.
        """
        return _items_sorted_by_keys(self, reverse=reverse)

    def items_sorted_by_values(self, reverse=False):
        """
        Return items (key/value list) sorted by values.
        If reverse is True, the list will be reversed.
        """
        return _items_sorted_by_values(self, reverse=reverse)

    def keypaths(self, indexes=False):
        """
        Return a list of all keypaths in the dict.
        If indexes is True, the output will include list values indexes.
        """
        return _keypaths(self, separator=self._keypath_separator, indexes=indexes)

    def match(self, pattern, indexes=True):
        """
        Return a list of all values whose keypath matches the given pattern (a regex or string).
        If pattern is string, wildcard can be used (eg. [*] can be used to match all list indexes).
        If indexes is True, the pattern will be matched also against list values.
        """
        return _match(self, pattern, separator=self._keypath_separator, indexes=indexes)

    def merge(self, other, *args, **kwargs):
        """
        Merge one or more dict objects into current instance (deepupdate).
        Sub-dictionaries will be merged toghether.
        If overwrite is False, existing values will not be overwritten.
        If concat is True, list values will be concatenated toghether.
        """
        _merge(self, other, *args, **kwargs)

    def move(self, key_src, key_dest):
        """
        Move a dict instance value item from 'key_src' to 'key_dst'.
        If key_dst exists, its value will be overwritten.
        """
        _move(self, key_src, key_dest)

    def nest(
        self, key, id_key="id", parent_id_key="parent_id", children_key="children"
    ):
        """
        Nest a list of dicts at the given key and return a new nested list
        using the specified keys to establish the correct items hierarchy.
        """
        return _nest(self[key], id_key, parent_id_key, children_key)

    def pop(self, key, *args):
        return self._cast(super(benedict, self).pop(key, *args))

    def remove(self, keys, *args):
        """
        Remove multiple keys from the current dict instance.
        It is possible to pass a single key or more keys (as list or *args).
        """
        _remove(self, keys, *args)

    def setdefault(self, key, default=None):
        return self._cast(super(benedict, self).setdefault(key, default))

    def rename(self, key, key_new):
        """
        Rename a dict item key from 'key' to 'key_new'.
        If key_new exists, a KeyError will be raised.
        """
        _rename(self, key, key_new)

    def search(
        self, query, in_keys=True, in_values=True, exact=False, case_sensitive=False
    ):
        """
        Search and return a list of items (dict, key, value, ) matching the given query.
        """
        return _search(self, query, in_keys, in_values, exact, case_sensitive)

    def standardize(self):
        """
        Standardize all dict keys (e.g. 'Location Latitude' -> 'location_latitude').
        """
        _standardize(self)

    def subset(self, keys, *args):
        """
        Return a new dict subset for the given keys.
        It is possible to pass a single key or multiple keys (as list or *args).
        """
        return _subset(self, keys, *args)

    def swap(self, key1, key2):
        """
        Swap items values at the given keys.
        """
        _swap(self, key1, key2)

    def traverse(self, callback):
        """
        Traverse the current dict instance (including nested dicts),
        and pass each item (dict, key, value) to the callback function.
        """
        _traverse(self, callback)

    def unflatten(self, separator="_"):
        """
        Return a new unflattened dict using the given separator
        to split dict keys to nested keypaths.
        """
        return _unflatten(self, separator)

    def unique(self):
        """
        Remove duplicated values from the current dict instance.
        """
        _unique(self)


# fix benedict json dumps support - #57 #59 #61
encoder.c_make_encoder = None

# fix benedict yaml representer - #43
SafeDumper.yaml_representers[benedict] = SafeRepresenter.represent_dict
