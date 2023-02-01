from benedict.core import clone as _clone


class BaseDict(dict):

    _dict = None
    _pointer = False

    @classmethod
    def _get_dict_or_value(cls, value):
        value = value.dict() if isinstance(value, cls) else value
        if isinstance(value, dict):
            for key in value.keys():
                key_val = value[key]
                if isinstance(key_val, cls):
                    key_val = cls._get_dict_or_value(value[key])
                    value[key] = key_val
        return value

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            self._dict = self._get_dict_or_value(args[0])
            self._pointer = True
            super().__init__(self._dict)
            return
        self._dict = None
        self._pointer = False
        super().__init__(*args, **kwargs)

    def __bool__(self):
        if self._pointer:
            return bool(self._dict)
        return len(self.keys()) > 0

    def __contains__(self, key):
        if self._pointer:
            return key in self._dict
        return super().__contains__(key)

    def __deepcopy__(self, memo):
        obj = self.__class__()
        for key, value in self.items():
            obj[key] = _clone(value, memo=memo)
        return obj

    def __delitem__(self, key):
        if self._pointer:
            del self._dict[key]
            return
        super().__delitem__(key)

    def __eq__(self, other):
        if self._pointer:
            return self._dict == other
        return super().__eq__(other)

    def __getitem__(self, key):
        if self._pointer:
            return self._dict[key]
        return super().__getitem__(key)

    def __iter__(self):
        if self._pointer:
            return iter(self._dict)
        return super().__iter__()

    def __len__(self):
        if self._pointer:
            return len(self._dict)
        return super().__len__()

    def __repr__(self):
        if self._pointer:
            return repr(self._dict)
        return super().__repr__()

    def __setitem__(self, key, value):
        value = self._get_dict_or_value(value)
        if self._pointer:
            is_dict_item = key in self._dict and isinstance(self._dict[key], dict)
            is_dict_value = isinstance(value, dict)
            if is_dict_item and is_dict_value:
                self._dict[key].clear()
                self._dict[key].update(value)
                return
            self._dict[key] = value
            return
        super().__setitem__(key, value)

    def __str__(self):
        if self._pointer:
            return str(self._dict)
        return super().__str__()

    def clear(self):
        if self._pointer:
            self._dict.clear()
            return
        super().clear()

    def copy(self):
        if self._pointer:
            return self._dict.copy()
        return super().copy()

    def dict(self):
        if self._pointer:
            return self._dict
        return self

    def get(self, key, default=None):
        if self._pointer:
            return self._dict.get(key, default)
        return super().get(key, default)

    def items(self):
        if self._pointer:
            return self._dict.items()
        return super().items()

    def keys(self):
        if self._pointer:
            return self._dict.keys()
        return super().keys()

    def pop(self, key, *args):
        if self._pointer:
            return self._dict.pop(key, *args)
        return super().pop(key, *args)

    def setdefault(self, key, default=None):
        default = self._get_dict_or_value(default)
        if self._pointer:
            return self._dict.setdefault(key, default)
        return super().setdefault(key, default)

    def update(self, other):
        other = self._get_dict_or_value(other)
        if self._pointer:
            self._dict.update(other)
            return
        super().update(other)

    def values(self):
        if self._pointer:
            return self._dict.values()
        return super().values()
