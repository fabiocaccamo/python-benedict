# -*- coding: utf-8 -*-

from benedict.utils import keylist_util, type_util


class KeylistDict(dict):

    def __init__(self, *args, **kwargs):
        super(KeylistDict, self).__init__(*args, **kwargs)

    def __contains__(self, key):
        if type_util.is_list_or_tuple(key):
            return self._contains_by_keys(key)
        return super(KeylistDict, self).__contains__(key)

    def _contains_by_keys(self, keys):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return key in parent
        elif type_util.is_list(parent):
            try:
                parent[key]
                return True
            except IndexError:
                return False
        return False

    def __delitem__(self, key):
        if type_util.is_list_or_tuple(key):
            self._delitem_by_keys(key)
            return
        super(KeylistDict, self).__delitem__(key)

    def _delitem_by_keys(self, keys):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            del parent[key]
            return
        elif type_util.is_list(parent):
            del parent[key]
            return
        raise KeyError

    def __getitem__(self, key):
        if type_util.is_list_or_tuple(key):
            return self._getitem_by_keys(key)
        return super(KeylistDict, self).__getitem__(key)

    def _getitem_by_keys(self, keys):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent[key]
        elif type_util.is_list(parent):
            return parent[key]
        raise KeyError

    def __setitem__(self, key, value):
        if type_util.is_list_or_tuple(key):
            self._setitem_by_keys(key, value)
            return
        super(KeylistDict, self).__setitem__(key, value)

    def _setitem_by_keys(self, keys, value):
        keylist_util.set_item(self, keys, value)

    def get(self, key, default=None):
        if type_util.is_list_or_tuple(key):
            return self._get_by_keys(key, default)
        return super(KeylistDict, self).get(key, default)

    def _get_by_keys(self, keys, default=None):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent.get(key, default)
        elif type_util.is_list(parent):
            return parent[key]
        return default

    def pop(self, key, *args):
        if type_util.is_list_or_tuple(key):
            return self._pop_by_keys(key, *args)
        return super(KeylistDict, self).pop(key, *args)

    def _pop_by_keys(self, keys, *args):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent.pop(key, *args)
        elif type_util.is_list(parent):
            return parent.pop(key)
        if args:
            return args[0]
        raise KeyError
