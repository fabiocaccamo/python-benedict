# -*- coding: utf-8 -*-


class BaseDict(dict):

    _dict = None
    _pointer = False

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = (
                args[0].dict() if issubclass(type(args[0]), BaseDict) else args[0]
            )
            self._pointer = True
            super(BaseDict, self).__init__(self._dict)
            return
        self._dict = None
        self._pointer = False
        super(BaseDict, self).__init__(*args, **kwargs)

    def __bool__(self):
        if self._pointer:
            return bool(self._dict)
        return len(self.keys()) > 0

    def __contains__(self, key):
        if self._pointer:
            return key in self._dict
        return super(BaseDict, self).__contains__(key)

    def __delitem__(self, key):
        if self._pointer:
            del self._dict[key]
            return
        super(BaseDict, self).__delitem__(key)

    def __eq__(self, other):
        if self._pointer:
            return self._dict == other
        return super(BaseDict, self).__eq__(other)

    def __getitem__(self, key):
        if self._pointer:
            return self._dict[key]
        return super(BaseDict, self).__getitem__(key)

    def __iter__(self):
        if self._pointer:
            return iter(self._dict)
        return super(BaseDict, self).__iter__()

    def __len__(self):
        if self._pointer:
            return len(self._dict)
        return super(BaseDict, self).__len__()

    def __repr__(self):
        if self._pointer:
            return repr(self._dict)
        return super(BaseDict, self).__repr__()

    def __setitem__(self, key, value):
        if self._pointer:
            self._dict[key] = value
            return
        super(BaseDict, self).__setitem__(key, value)

    def __str__(self):
        if self._pointer:
            return str(self._dict)
        return super(BaseDict, self).__str__()

    def clear(self):
        if self._pointer:
            self._dict.clear()
            return
        super(BaseDict, self).clear()

    def copy(self):
        if self._pointer:
            return self._dict.copy()
        return super(BaseDict, self).copy()

    def dict(self):
        if self._pointer:
            return self._dict
        return self

    def get(self, key, default=None):
        if self._pointer:
            return self._dict.get(key, default)
        return super(BaseDict, self).get(key, default)

    def items(self):
        if self._pointer:
            return self._dict.items()
        return super(BaseDict, self).items()

    def keys(self):
        if self._pointer:
            return self._dict.keys()
        return super(BaseDict, self).keys()

    def pop(self, key, *args):
        if self._pointer:
            return self._dict.pop(key, *args)
        return super(BaseDict, self).pop(key, *args)

    def setdefault(self, key, default=None):
        if self._pointer:
            return self._dict.setdefault(key, default)
        return super(BaseDict, self).setdefault(key, default)

    def update(self, other):
        if self._pointer:
            self._dict.update(other)
            return
        super(BaseDict, self).update(other)

    def values(self):
        if self._pointer:
            return self._dict.values()
        return super(BaseDict, self).values()
