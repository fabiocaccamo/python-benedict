# -*- coding: utf-8 -*-


class BaseDict(dict):

    _dict = None

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = args[0]
            super(BaseDict, self).__init__(self._dict)
            return
        self._dict = None
        super(BaseDict, self).__init__(*args, **kwargs)

    def _is_pointer(self):
        return self._dict is not self and self._dict is not None

    def __contains__(self, key):
        if self._is_pointer():
            return key in self._dict
        return super(BaseDict, self).__contains__(key)

    def __delitem__(self, key):
        if self._is_pointer():
            del self._dict[key]
            return
        super(BaseDict, self).__delitem__(key)

    def __eq__(self, other):
        if self._is_pointer():
            return self._dict == other
        return super(BaseDict, self).__eq__(other)

    def __getitem__(self, key):
        if self._is_pointer():
            return self._dict[key]
        return super(BaseDict, self).__getitem__(key)

    def __iter__(self):
        if self._is_pointer():
            return iter(self._dict)
        return super(BaseDict, self).__iter__()

    def __len__(self):
        if self._is_pointer():
            return len(self._dict)
        return super(BaseDict, self).__len__()

    def __repr__(self):
        if self._is_pointer():
            return repr(self._dict)
        return super(BaseDict, self).__repr__()

    def __setitem__(self, key, value):
        if self._is_pointer():
            self._dict[key] = value
            return
        super(BaseDict, self).__setitem__(key, value)

    def __str__(self):
        if self._is_pointer():
            return str(self._dict)
        return super(BaseDict, self).__str__()

    def __unicode__(self):
        if self._is_pointer():
            return unicode(self._dict)
        return super(BaseDict, self).__unicode__()

    def clear(self):
        if self._is_pointer():
            self._dict.clear()
            return
        super(BaseDict, self).clear()

    def copy(self):
        if self._is_pointer():
            return self._dict.copy()
        return super(BaseDict, self).copy()

    def dict(self):
        if self._is_pointer():
            return self._dict
        return self

    def get(self, key, default=None):
        if self._is_pointer():
            return self._dict.get(key, default)
        return super(BaseDict, self).get(key, default)

    def items(self):
        if self._is_pointer():
            return self._dict.items()
        return super(BaseDict, self).items()

    def keys(self):
        if self._is_pointer():
            return self._dict.keys()
        return super(BaseDict, self).keys()

    def pop(self, key, *args):
        if self._is_pointer():
            return self._dict.pop(key, *args)
        return super(BaseDict, self).pop(key, *args)

    def setdefault(self, key, default=None):
        if self._is_pointer():
            return self._dict.setdefault(key, default)
        return super(BaseDict, self).setdefault(key, default)

    def update(self, other):
        if self._is_pointer():
            self._dict.update(other)
            return
        super(BaseDict, self).update(other)

    def values(self):
        if self._is_pointer():
            return self._dict.values()
        return super(BaseDict, self).values()
