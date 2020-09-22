# -*- coding: utf-8 -*-


class BaseDict(dict):

    _dict = {}

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = args[0]
        else:
            self._dict = dict(*args, **kwargs)
        super(BaseDict, self).__init__(*args, **kwargs)

    def __bool__(self):
        return bool(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __delitem__(self, key):
        del self._dict[key]
        super(BaseDict, self).__delitem__(key)

    def __eq__(self, other):
        return self._dict == other

    def __getitem__(self, key):
        return self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __nonzero__(self):
        return bool(self._dict)

    def __repr__(self):
        return repr(self._dict)

    def __setitem__(self, key, value):
        self._dict[key] = value
        super(BaseDict, self).__setitem__(key, value)

    def __str__(self):
        return str(self._dict)

    def __unicode__(self):
        return unicode(self._dict)

    def clear(self):
        self._dict.clear()
        super(BaseDict, self).clear()

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
        value = self._dict.pop(key, *args)
        super(BaseDict, self).pop(key, None)
        return value

    def setdefault(self, key, default=None):
        value = self._dict.setdefault(key, default)
        super(BaseDict, self).setdefault(key, default)
        return value

    def update(self, other):
        self._dict.update(other)
        super(BaseDict, self).update(other)

    def values(self):
        return self._dict.values()
