from __future__ import annotations

from collections.abc import Sequence
from typing import Any, cast

from typing_extensions import TypeVar

from benedict.dicts.base import BaseDict
from benedict.dicts.keylist import keylist_util
from benedict.utils import type_util

_T = TypeVar("_T")
_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)


class KeylistDict(BaseDict[list[str | int] | tuple[str | int, ...] | _K, _V]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __contains__(self, key: object) -> bool:
        if type_util.is_list(key):
            return self._contains_bystreys(key)
        return super().__contains__(key)

    def _contains_bystreys(self, keys: Sequence[_K]) -> bool:
        parent, _, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict_or_list_or_tuple(parent):
            return True
        return False

    def __delitem__(self, key: _K | list[Any] | tuple[str | int, ...]) -> None:
        if type_util.is_list(key):
            self._delitem_bystreys(key)
            return
        super().__delitem__(key)

    def _delitem_bystreys(self, keys: Any) -> None:
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict_or_list(parent):
            del parent[key]
            return
        elif type_util.is_tuple(parent):
            # raise the standard TypeError
            del parent[key]  # type: ignore[unreachable]
        raise KeyError(f"Invalid keys: {keys!r}")

    def __getitem__(self, key: list[str | int] | _K) -> _V:  # type: ignore[override]
        if type_util.is_list(key):
            return cast("_V", self._getitem_bystreys(key))
        return super().__getitem__(key)

    def _getitem_bystreys(self, keys: Any) -> Any:
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict_or_list_or_tuple(parent):
            return parent[key]
        raise KeyError(f"Invalid keys: {keys!r}")

    def __setitem__(
        self, key: list[str | int] | tuple[str | int, ...] | _K, value: _V
    ) -> None:
        if type_util.is_list(key):
            self._setitem_bystreys(key, value)
            return
        super().__setitem__(key, value)

    def _setitem_bystreys(self, keys: Any, value: _V) -> None:
        keylist_util.set_item(self, keys, value)

    def get(  # type: ignore[override]
        self,
        key: list[str | int] | tuple[str | int, ...] | _K,
        default: _V | None = None,
    ) -> _V | None:
        if type_util.is_list(key):
            return cast("_V | None", self._get_bystreys(key, default))
        return super().get(key, default)

    def _get_bystreys(self, keys: Any, default: _T | _V | None = None) -> Any:
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent.get(key, default)
        elif type_util.is_list_or_tuple(parent):
            return parent[key]  # type: ignore[unreachable]
        return default

    def pop(self, key: _K | list[str], *args: Any) -> Any:  # type: ignore[override]
        if type_util.is_list(key):
            return self._pop_bystreys(key, *args)
        return super().pop(key, *args)

    def _pop_bystreys(self, keys: Sequence[Any], *args: Any) -> Any:
        parent, key, _ = keylist_util.get_item(self, keys)
        if type_util.is_dict(parent):
            return parent.pop(key, *args)
        elif type_util.is_list(parent):
            return parent.pop(key)  # type: ignore[unreachable]
        elif type_util.is_tuple(parent):
            # raise the standard TypeError
            del parent[key]  # type: ignore[unreachable]
        if args:
            return args[0]
        raise KeyError(f"Invalid keys: {keys!r}")

    def set(self, key: _K, value: _V) -> None:
        self[key] = value

    def setdefault(  # type: ignore[override]
        self,
        key: list[str | int] | tuple[str | int, ...] | _K,
        default: _V | None = None,
    ) -> _V | None:
        if key not in self:
            self[key] = default  # type: ignore[assignment]
            return default
        return self[key]  # type: ignore[index]
