from __future__ import annotations

from collections.abc import (
    ItemsView,
    Iterator,
    KeysView,
    Mapping,
    MutableMapping,
    ValuesView,
)
from typing import Any, cast

from typing_extensions import Self, TypeVar

from benedict.core.clone import clone as _clone

_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)


class BaseDict(dict[_K, _V]):
    _dict: dict[_K, _V] | None = None

    @classmethod
    def _get_dict_or_value(cls, value: Any) -> Any:
        value = value.dict() if isinstance(value, cls) else value
        if isinstance(value, MutableMapping):
            for key in value.keys():
                key_val = value[key]
                if isinstance(key_val, cls):
                    key_val = cls._get_dict_or_value(value[key])
                    value[key] = key_val
        return value

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._dict = None
        if len(args) == 1 and isinstance(args[0], Mapping):
            self._dict = self._get_dict_or_value(args[0])
            super().__init__(self._dict)
            return
        super().__init__(*args, **kwargs)

    def __bool__(self) -> bool:
        if self._dict is not None:
            return bool(self._dict)
        return len(self.keys()) > 0

    def __contains__(self, o: object) -> bool:
        if self._dict is not None:
            return o in self._dict
        return super().__contains__(o)

    def __deepcopy__(self, memo: dict[int, Any]) -> Self:
        obj = self.__class__()
        for key, value in self.items():
            obj[key] = _clone(value, memo=memo)
        return obj

    def __delitem__(self, key: _K) -> None:
        if self._dict is not None:
            del self._dict[key]
            return
        super().__delitem__(key)

    def __eq__(self, other: object) -> bool:
        if self._dict is not None:
            return self._dict == other
        return super().__eq__(other)

    def __getitem__(self, key: _K) -> _V:
        if self._dict is not None:
            return self._dict[key]
        return super().__getitem__(key)

    def __ior__(self, other: Any) -> Self:  # type: ignore[misc,override]
        if self._dict is not None:
            return cast("Self", self._dict.__ior__(other))
        return super().__ior__(other)

    def __iter__(self) -> Iterator[_K]:
        if self._dict is not None:
            return iter(self._dict)
        return super().__iter__()

    def __len__(self) -> int:
        if self._dict is not None:
            return len(self._dict)
        return super().__len__()

    def __or__(self, other: dict[_K, _V]) -> Self:  # type: ignore[override]
        if self._dict is not None:
            return cast("Self", self._dict.__or__(other))
        return cast("Self", super().__or__(other))

    def __repr__(self) -> str:
        if self._dict is not None:
            return repr(self._dict)
        return super().__repr__()

    def __setitem__(self, key: _K, value: _V) -> None:
        value = self._get_dict_or_value(value)
        if self._dict is not None:
            is_dict_item = key in self._dict and isinstance(self._dict[key], dict)
            is_dict_value = isinstance(value, dict)
            if is_dict_item and is_dict_value:
                if self._dict[key] is value:
                    # prevent clearing dict instance when assigning value to itself. fix #294
                    return
                self._dict[key].clear()  # type: ignore[attr-defined]
                self._dict[key].update(value)  # type: ignore[attr-defined]
                return
            self._dict[key] = value
            return
        super().__setitem__(key, value)

    def __setstate__(self, state: Mapping[str, Any]) -> None:
        self._dict = state["_dict"]
        self._dict = state["_dict"]

    def __str__(self) -> str:
        if self._dict is not None:
            return str(self._dict)
        return super().__str__()

    def clear(self) -> None:
        if self._dict is not None:
            self._dict.clear()
            return
        super().clear()

    def copy(self) -> Self:
        if self._dict is not None:
            return cast("Self", self._dict.copy())
        return cast("Self", super().copy())

    def dict(self) -> Self:
        if self._dict is not None:
            return cast("Self", self._dict)
        return self

    def get(self, key: _K, default: _V | None = None) -> _V | None:  # type: ignore[override]
        if self._dict is not None:
            return self._dict.get(key, default)
        return super().get(key, default)

    def items(self) -> ItemsView[_K, _V]:  # type: ignore[override]
        if self._dict is not None:
            return self._dict.items()
        return super().items()

    def keys(self) -> KeysView[_K]:  # type: ignore[override]
        if self._dict is not None:
            return self._dict.keys()
        return super().keys()

    def pop(self, key: _K, *args: Any) -> _V:
        if self._dict is not None:
            return self._dict.pop(key, *args)  # type: ignore[no-any-return]
        return super().pop(key, *args)  # type: ignore[no-any-return]

    def setdefault(self, key: _K, default: _V | None = None) -> _V:
        default = self._get_dict_or_value(default)
        assert default is not None
        if self._dict is not None:
            return self._dict.setdefault(key, default)
        return super().setdefault(key, default)

    def update(self, other: Any) -> None:
        other = self._get_dict_or_value(other)
        if self._dict is not None:
            self._dict.update(other)
            return
        super().update(other)

    def values(self) -> ValuesView[_V]:  # type: ignore[override]
        if self._dict is not None:
            return self._dict.values()
        return super().values()
