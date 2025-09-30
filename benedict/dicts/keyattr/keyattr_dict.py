from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

from typing_extensions import TypeVar

from benedict.dicts.base import BaseDict

_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)


class KeyattrDict(BaseDict[_K, _V]):
    _keyattr_enabled: bool | None = None
    _keyattr_dynamic: bool | None = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._keyattr_enabled = kwargs.pop("keyattr_enabled", True)
        self._keyattr_dynamic = kwargs.pop("keyattr_dynamic", False)
        super().__init__(*args, **kwargs)

    @property
    def keyattr_enabled(self) -> bool | None:
        return self._keyattr_enabled

    @keyattr_enabled.setter
    def keyattr_enabled(self, value: bool) -> None:
        self._keyattr_enabled = value

    @property
    def keyattr_dynamic(self) -> bool | None:
        return self._keyattr_dynamic

    @keyattr_dynamic.setter
    def keyattr_dynamic(self, value: bool) -> None:
        self._keyattr_dynamic = value

    def __getattr__(self, attr: _K | str) -> Any:
        attr_message = f"{self.__class__.__name__!r} object has no attribute {attr!r}"
        attr_k = cast("_K", attr)
        if not self._keyattr_enabled:
            raise AttributeError(attr_message)
        try:
            return self.__getitem__(attr_k)
        except KeyError:
            if isinstance(attr, str) and attr.startswith("_"):
                raise AttributeError(attr_message) from None
            if not self._keyattr_dynamic:
                raise AttributeError(attr_message) from None
            self.__setitem__(attr_k, cast("_V", {}))
            return self.__getitem__(attr_k)

    def __setattr__(self, attr: _K | str, value: Any) -> None:
        attr_message = f"{self.__class__.__name__!r} object has no attribute {attr!r}"
        attr_k = cast("_K", attr)
        if attr in self:
            # set existing key
            if not self._keyattr_enabled:
                raise AttributeError(attr_message)
            self.__setitem__(attr_k, value)
        elif isinstance(attr, str) and hasattr(self.__class__, attr):
            # set existing attr
            super().__setattr__(attr, value)
        else:
            # set new key
            if not self._keyattr_enabled:
                raise AttributeError(attr_message)
            self.__setitem__(attr_k, value)

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        super().__setstate__(state)
        self._keyattr_enabled = state["_keyattr_enabled"]
        self._keyattr_dynamic = state["_keyattr_dynamic"]
