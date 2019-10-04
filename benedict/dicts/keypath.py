# -*- coding: utf-8 -*-

from benedict.utils import keypath_util


class KeypathDict(dict):

    def __init__(self, *args, **kwargs):
        self._keypath_separator = kwargs.pop('keypath_separator', None) \
            if 'keypath_separator' in kwargs else '.'
        super(KeypathDict, self).__init__(*args, **kwargs)
        self._check_keys(self)

    def _check_keys(self, d):
        keys = keypath_util.all_keys(d)
        keypath_util.check_keys(keys, self._keypath_separator)

    def _follow_keys(self, keys):
        return keypath_util.follow_keys(self, keys)

    def _join_keys(self, keys):
        return keypath_util.join_keys(keys, self._keypath_separator)

    def _split_keys(self, key):
        return keypath_util.split_keys(key, self._keypath_separator)

    def __contains__(self, key):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._follow_keys(keys)
            if isinstance(item_parent, dict):
                if item_parent.__contains__(item_key):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return super(KeypathDict, self).__contains__(key)

    def __delitem__(self, key):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._follow_keys(keys)
            if isinstance(item_parent, dict):
                item_parent.__delitem__(item_key)
            else:
                raise KeyError
        else:
            super(KeypathDict, self).__delitem__(key)

    def __getitem__(self, key):
        keys = self._split_keys(key)
        value = None
        if len(keys) > 1:
            item_parent, item_key = self._follow_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent.__getitem__(item_key)
            else:
                raise KeyError
        else:
            value = super(KeypathDict, self).__getitem__(key)
        return value

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._check_keys(value)
        keys = self._split_keys(key)
        if len(keys) > 1:
            i = 0
            j = len(keys)
            item = self
            while i < j:
                key = keys[i]
                if i < (j - 1):
                    if item is self:
                        subitem = super(KeypathDict, self).get(key, None)
                    else:
                        subitem = item.get(key, None)
                    if not isinstance(subitem, dict):
                        subitem = item[key] = {}
                    item = subitem
                else:
                    item[key] = value
                i += 1
        else:
            super(KeypathDict, self).__setitem__(key, value)

    @classmethod
    def fromkeys(cls, sequence, value=None):
        d = KeypathDict()
        for key in sequence:
            d[key] = value
        return d

    def get(self, key, default=None):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._follow_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent.get(item_key, default)
            else:
                return default
        else:
            return super(KeypathDict, self).get(key, default)

    def keypaths(self):
        if not self._keypath_separator:
            return []
        def walk_keypaths(root, path):
            keypaths = []
            for key, value in root.items():
                keys = path + [key]
                keypaths += [self._join_keys(keys)]
                if isinstance(value, dict):
                    keypaths += walk_keypaths(value, keys)
            return keypaths
        keypaths = walk_keypaths(self, [])
        keypaths.sort()
        return keypaths

    def pop(self, key, *args, **kwargs):
        if kwargs and 'default' in kwargs:
            default_arg = True
            default = kwargs.get('default', None)
        elif args:
            default_arg = True
            default = args[0]
        else:
            default_arg = False
            default = None
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._follow_keys(keys)
            if isinstance(item_parent, dict):
                if default_arg:
                    return item_parent.pop(item_key, default)
                else:
                    return item_parent.pop(item_key)
            else:
                if default_arg:
                    return default
                else:
                    raise KeyError
        else:
            if default_arg:
                return super(KeypathDict, self).pop(key, default)
            else:
                return super(KeypathDict, self).pop(key)

    def set(self, key, value):
        self.__setitem__(key, value)

    def setdefault(self, key, default=None):
        if key not in self:
            self.__setitem__(key, default)
            return default
        else:
            return self.__getitem__(key)

    def update(self, other):
        if isinstance(other, dict):
            self._check_keys(other)
        super(KeypathDict, self).update(other)
