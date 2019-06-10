# -*- coding: utf-8 -*-

from six import string_types


class KeypathDict(dict):

    def __init__(self, *args, **kwargs):
        self._separator = kwargs.pop('separator', '.')
        super(KeypathDict, self).__init__(*args, **kwargs)

    @staticmethod
    def _join_keys(keys, separator):
        return separator.join(keys)

    @staticmethod
    def _split_keys(key, separator):
        if isinstance(key, string_types):
            keypath = key
            if separator in keypath:
                keys = list(keypath.split(separator))
                return keys
            else:
                return [key]
        elif isinstance(key, (list, tuple, )):
            keys = []
            for key_item in key:
                keys += KeypathDict._split_keys(key_item, separator)
            return keys
        else:
            return [key]

    def _get_value_by_keys(self, keys):
        i = 0
        j = len(keys)
        val = self
        while i < j:
            key = keys[i]
            try:
                val = val[key]
            except KeyError:
                val = None
                break
            i += 1
        return val

    def _get_value_context_by_keys(self, keys):
        item_keys = keys[:-1]
        item_key = keys[-1]
        item_parent = self._get_value_by_keys(item_keys)
        return (item_parent, item_key, )

    def _has_value_by_keys(self, keys):
        item_parent, item_key = self._get_value_context_by_keys(keys)
        if isinstance(item_parent, dict):
            if item_key in item_parent:
                return True
            else:
                return False
        else:
            return False

    def _set_value_by_keys(self, keys, value):
        i = 0
        j = len(keys)
        item = self
        while i < j:
            key = keys[i]
            if i < (j - 1):
                if item == self:
                    subitem = super(KeypathDict, self).get(key, None)
                else:
                    subitem = item.get(key, None)
                if not isinstance(subitem, dict):
                    subitem = item[key] = {}
                item = subitem
            else:
                item[key] = value
            i += 1

    def __contains__(self, key):
        keys = self._split_keys(key, self._separator)
        if len(keys) > 1:
            return self._has_value_by_keys(keys)
        else:
            return super(KeypathDict, self).__contains__(key)

    def __delitem__(self, key):
        keys = self._split_keys(key, self._separator)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                del item_parent[item_key]
            else:
                raise KeyError
        else:
            super(KeypathDict, self).__delitem__(key)

    def __getitem__(self, key):
        keys = self._split_keys(key, self._separator)
        value = None
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent[item_key]
            else:
                raise KeyError
        else:
            value = super(KeypathDict, self).__getitem__(key)
        return value

    def __setitem__(self, key, value):
        keys = self._split_keys(key, self._separator)
        if len(keys) > 1:
            self._set_value_by_keys(keys, value)
        else:
            super(KeypathDict, self).__setitem__(key, value)

    @classmethod
    def fromkeys(cls, sequence, value=None):
        d = KeypathDict()
        for key in sequence:
            d[key] = value
        return d

    def get(self, key, default=None):
        keys = self._split_keys(key, self._separator)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent.get(item_key, default)
            else:
                return default
        else:
            return super(KeypathDict, self).get(key, default)

    def keypaths(self):
        def walk_keypaths(root, path):
            keypaths = []
            for key, val in root.items():
                keypaths += [self._join_keys(path + [key], self._separator)]
                if isinstance(val, dict):
                    keypaths += walk_keypaths(val, path + [key])
            return keypaths
        keypaths = walk_keypaths(self, [])
        keypaths.sort()
        return keypaths

    def pop(self, key, default=None):
        keys = self._split_keys(key, self._separator)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                if default is None:
                    return item_parent.pop(item_key)
                else:
                    return item_parent.pop(item_key, default)
            else:
                if default is None:
                    raise KeyError
                else:
                    return default
        else:
            if default is None:
                return super(KeypathDict, self).pop(key)
            else:
                return super(KeypathDict, self).pop(key, default)

    def set(self, key, value):
        self[key] = value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
            return default
        else:
            return self[key]

