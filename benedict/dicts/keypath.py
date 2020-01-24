# -*- coding: utf-8 -*-

from benedict.utils import dict_util, keypath_util


class KeypathDict(dict):

    _keypath_separator = None

    def __init__(self, *args, **kwargs):
        """
        Constructs a new instance.
        """
        self._keypath_separator = kwargs.pop('keypath_separator', '.')
        super(KeypathDict, self).__init__(*args, **kwargs)
        keypath_util.check_keys(self, self._keypath_separator)

    @property
    def keypath_separator(self):
        return self._keypath_separator

    @keypath_separator.setter
    def keypath_separator(self, value):
        keypath_util.check_keys(self, value)
        self._keypath_separator = value

    def __contains__(self, key):
        keys = keypath_util.list_keys(key, self._keypath_separator)
        if len(keys) > 1:
            return self.__contains_by_keys(keys)
        key = keys[0]
        return super(KeypathDict, self).__contains__(key)

    def __contains_by_keys(self, keys):
        parent, key, _ = dict_util.resolve(self, keys)[-1]
        if isinstance(parent, dict) and key in parent:
            return True
        return False

    def __delitem__(self, key):
        keys = keypath_util.list_keys(key, self._keypath_separator)
        if len(keys) > 1:
            self.__delitem_by_keys(keys)
            return
        key = keys[0]
        super(KeypathDict, self).__delitem__(key)

    def __delitem_by_keys(self, keys):
        parent, key, _ = dict_util.resolve(self, keys)[-1]
        if isinstance(parent, dict):
            del parent[key]
            return
        raise KeyError

    def __getitem__(self, key):
        keys = keypath_util.list_keys(key, self._keypath_separator)
        value = None
        if len(keys) > 1:
            return self.__getitem_by_keys(keys)
        key = keys[0]
        return super(KeypathDict, self).__getitem__(key)

    def __getitem_by_keys(self, keys):
        parent, key, _ = dict_util.resolve(self, keys)[-1]
        if isinstance(parent, dict):
            return parent[key]
        raise KeyError

    def __setitem__(self, key, value):
        keypath_util.check_keys(value, self._keypath_separator)
        keys = keypath_util.list_keys(key, self._keypath_separator)
        if len(keys) > 1:
            self.__setitem_by_keys(keys, value)
            return
        key = keys[0]
        super(KeypathDict, self).__setitem__(key, value)

    def __setitem_by_keys(self, keys, value):
        i = 0
        j = len(keys)
        item = self
        while i < j:
            key = keys[i]
            if i < (j - 1):
                subitem = item.get(key, None)
                if not isinstance(subitem, dict):
                    subitem = item[key] = {}
                item = subitem
                i += 1
                continue
            item[key] = value
            break

    @classmethod
    def fromkeys(cls, sequence, value=None):
        d = cls()
        for key in sequence:
            d[key] = value
        return d

    def get(self, key, default=None):
        keys = keypath_util.list_keys(key, self._keypath_separator)
        if len(keys) > 1:
            return self.__get_by_keys(keys, default)
        key = keys[0]
        return super(KeypathDict, self).get(key, default)

    def __get_by_keys(self, keys, default=None):
        parent, key, _ = dict_util.resolve(self, keys)[-1]
        if isinstance(parent, dict):
            return parent.get(key, default)
        return default

    def pop(self, key, *args):
        keys = keypath_util.list_keys(key, self._keypath_separator)
        if len(keys) > 1:
            return self.__pop_by_keys(keys, *args)
        return super(KeypathDict, self).pop(key, *args)

    def __pop_by_keys(self, keys, *args):
        parent, key, _ = dict_util.resolve(self, keys)[-1]
        if isinstance(parent, dict):
            return parent.pop(key, *args)
        if args:
            # default
            return args[0]
        raise KeyError

    def set(self, key, value):
        self.__setitem__(key, value)

    def setdefault(self, key, default=None):
        if key not in self:
            self.__setitem__(key, default)
            return default
        return self.__getitem__(key)

    def update(self, other):
        keypath_util.check_keys(other, self._keypath_separator)
        super(KeypathDict, self).update(other)
