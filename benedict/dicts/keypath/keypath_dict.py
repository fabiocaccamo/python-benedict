from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from typing_extensions import Self, TypeVar

from benedict.dicts import KeylistDict
from benedict.dicts.keypath import keypath_util

_K = keypath_util.KeyType
_V = TypeVar("_V", default=Any)


class KeypathDict(KeylistDict[_K, _V]):
    _keypath_separator: str | None = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._keypath_separator = kwargs.pop("keypath_separator", ".")
        check_keys = kwargs.pop("check_keys", True)
        super().__init__(*args, **kwargs)
        if check_keys:
            keypath_util.check_keys(self, self._keypath_separator)

    @property
    def keypath_separator(self) -> str | None:
        return self._keypath_separator

    @keypath_separator.setter
    def keypath_separator(self, value: str) -> None:
        keypath_util.check_keys(self, value)
        self._keypath_separator = value

    def __contains__(self, key: object) -> bool:
        return super().__contains__(self._parse_key(key))  # type: ignore[arg-type]

    def __delitem__(self, key: object) -> None:
        super().__delitem__(self._parse_key(key))  # type: ignore[arg-type]

    def __getitem__(self, key: _K) -> _V:
        return super().__getitem__(self._parse_key(key))

    def __setitem__(self, key: _K, value: _V) -> None:
        keypath_util.check_keys(value, self._keypath_separator)
        super().__setitem__(self._parse_key(key), value)

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        super().__setstate__(state)
        self._keypath_separator = state["_keypath_separator"]

    def _parse_key(self, key: _K) -> _K:
        keys = keypath_util.parse_keys(key, self._keypath_separator)
        keys_count = len(keys)
        if keys_count == 0:
            return None
        elif keys_count == 1:
            return keys[0]
        return keys

    @classmethod
    def fromkeys(  # type: ignore[override]
        cls, sequence: Iterable[_K], value: _V | None = None
    ) -> Self:
        d = cls()
        for key in sequence:
            d[key] = value  # type: ignore[assignment]
        return d

    def get(self, key: _K, default: _V | None = None) -> _V | None:  # type: ignore[override]
        return super().get(self._parse_key(key), default)

    def pop(self, key: _K, *args: Any) -> _V:  # type: ignore[override]
        return super().pop(self._parse_key(key), *args)  # type: ignore[no-any-return]

    def update(self, other: Mapping[Any, _V]) -> None:  # type: ignore[override]
        keypath_util.check_keys(other, self._keypath_separator)
        super().update(other)
