# -*- coding: utf-8 -*-

from benedict.dicts import KeylistDict
from benedict.dicts.keypath import keypath_util


class KeypathDict(KeylistDict):

    _keypath_separator = None

    def __init__(self, *args, **kwargs):
        self._keypath_separator = kwargs.pop("keypath_separator", ".")
        check_keys = kwargs.pop("check_keys", True)
        super(KeypathDict, self).__init__(*args, **kwargs)
        if check_keys:
            keypath_util.check_keys(self, self._keypath_separator)

    @property
    def keypath_separator(self):
        return self._keypath_separator

    @keypath_separator.setter
    def keypath_separator(self, value):
        keypath_util.check_keys(self, value)
        self._keypath_separator = value

    def __contains__(self, key):
        return super(KeypathDict, self).__contains__(self._parse_key(key))

    def __delitem__(self, key):
        super(KeypathDict, self).__delitem__(self._parse_key(key))

    def __getitem__(self, key):
        return super(KeypathDict, self).__getitem__(self._parse_key(key))

    def __setitem__(self, key, value):
        keypath_util.check_keys(value, self._keypath_separator)
        super(KeypathDict, self).__setitem__(self._parse_key(key), value)

    def _parse_key(self, key):
        keys = keypath_util.parse_keys(key, self._keypath_separator)
        keys_count = len(keys)
        if keys_count == 0:
            return None
        elif keys_count == 1:
            return keys[0]
        return keys

    @classmethod
    def fromkeys(cls, sequence, value=None):
        d = cls()
        for key in sequence:
            d[key] = value
        return d

    def get(self, key, default=None):
        return super(KeypathDict, self).get(self._parse_key(key), default)

    def pop(self, key, *args):
        return super(KeypathDict, self).pop(self._parse_key(key), *args)

    def update(self, other):
        keypath_util.check_keys(other, self._keypath_separator)
        super(KeypathDict, self).update(other)
