from benedict.dicts.base import BaseDict


class KeyattrDict(BaseDict):
    _keyattr_enabled = None

    def __init__(self, *args, **kwargs):
        self._keyattr_enabled = kwargs.pop("keyattr_enabled", True)
        super().__init__(*args, **kwargs)

    @property
    def keyattr_enabled(self):
        return self._keyattr_enabled

    @keyattr_enabled.setter
    def keyattr_enabled(self, value):
        self._keyattr_enabled = value

    def __getattr__(self, attr):
        if not self._keyattr_enabled:
            raise AttributeError
        # return super().__getattr__(attr)
        try:
            return self.__getitem__(attr)
        except KeyError:
            if attr.startswith("_"):
                raise AttributeError(
                    f"{self.__class__.__name__!r} object has no attribute {attr!r}"
                ) from None
            self.__setitem__(attr, {})
            return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        if attr in self:
            # set existing key
            if not self._keyattr_enabled:
                raise AttributeError
            self.__setitem__(attr, value)
        elif hasattr(self.__class__, attr):
            # set existing attr
            super().__setattr__(attr, value)
        else:
            # set new key
            if not self._keyattr_enabled:
                raise AttributeError
            self.__setitem__(attr, value)

    def __setstate__(self, state):
        super().__setstate__(state)
        self._keyattr_enabled = state["_keyattr_enabled"]
