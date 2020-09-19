# -*- coding: utf-8 -*-


class BaseDict(dict):

    _dict = {}

    def __init__(self, *args, **kwargs):
        super(BaseDict, self).__init__()
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = args[0]
            return
        self._dict = dict(*args, **kwargs)

    def __bool__(self):
        return bool(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __delitem__(self, key):
        del self._dict[key]

    def __eq__(self, other):
        return self._dict == other

    def __getitem__(self, key):
        return self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __str__(self):
        return str(self._dict)

    def clear(self):
        self._dict.clear()

    def copy(self):
        return self._dict.copy()

    def dict(self):
        return self._dict

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def pop(self, key, *args):
        return self._dict.pop(key, *args)

    def setdefault(self, key, default=None):
        return self._dict.setdefault(key, default)

    def update(self, other):
        self._dict.update(other)

    def values(self):
        return self._dict.values()
