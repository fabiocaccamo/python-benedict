from benedict.dicts.base import BaseDict
from benedict.dicts.keylist import keylist_util
from benedict.utils import type_util


class KeylistDict(BaseDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __contains__(self, key):
        if type_util.is_list_or_tuple(key):
            return self._contains_by_keys(key)
        return super().__contains__(key)

    def _contains_by_keys(self, keys):
        parent, _, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict_or_list_or_tuple(parent):
            return True
        return False

    def __delitem__(self, key):
        if type_util.is_list_or_tuple(key):
            self._delitem_by_keys(key)
            return
        super().__delitem__(key)

    def _delitem_by_keys(self, keys):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_wildcard(key):
            self[keys[:-1]].clear()
            return
        elif type_util.is_dict_or_list(parent):
            del parent[key]
            return
        elif type_util.is_tuple(parent):
            # raise the standard TypeError
            del parent[key]
        raise KeyError(f"Invalid keys: '{keys}'")

    def __getitem__(self, key):
        if type_util.is_list_or_tuple(key):
            return self._getitem_by_keys(key)
        return super().__getitem__(key)

    def _getitem_by_keys(self, keys):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_list(parent) and type_util.is_wildcard(key):
            return parent
        if type_util.is_list_of_dicts(parent) and type_util.any_wildcard_in_list(keys):
            return [item.get(key) for item in parent]
        if type_util.is_dict_or_list_or_tuple(parent):
            return parent[key]
        raise KeyError(f"Invalid keys: '{keys}'")

    def __setitem__(self, key, value):
        if type_util.is_list_or_tuple(key):
            self._setitem_by_keys(key, value)
            return
        super().__setitem__(key, value)

    def _setitem_by_keys(self, keys, value):
        keylist_util.set_item(self, keys, value)

    def get(self, key, default=None):
        if type_util.is_list_or_tuple(key):
            return self._get_by_keys(key, default)
        return super().get(key, default)

    def _get_by_keys(self, keys, default=None):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_list(parent) and type_util.is_wildcard(key):
            return parent
        elif type_util.is_wildcard(keys[-2]):
            if type_util.is_list_of_dicts(parent):
                return [item.get(key) for item in parent]
            elif type_util.is_list_of_list(parent):
                return _
        elif type_util.is_dict(parent):
            return parent.get(key, default)
        elif type_util.is_list_or_tuple(parent):
            return parent[key]
        return default

    def pop(self, key, *args):
        if type_util.is_list_or_tuple(key):
            return self._pop_by_keys(key, *args)
        return super().pop(key, *args)

    def _pop_by_keys(self, keys, *args):
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent.pop(key, *args)
        elif type_util.is_list(parent) and type_util.is_wildcard(key):
            del self[keys[:-1]]
            return parent
        elif type_util.is_list_of_dicts(parent) and type_util.any_wildcard_in_list(
            keys
        ):
            return [_item.pop(key) if key in _item else None for _item in parent]
        elif type_util.is_list(parent):
            return parent.pop(key)
        elif type_util.is_tuple(parent):
            # raise the standard TypeError
            del parent[key]
        if args:
            return args[0]
        raise KeyError(f"Invalid keys: '{keys}'")

    def set(self, key, value):
        self[key] = value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
            return default
        return self[key]
