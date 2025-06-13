from __future__ import annotations

from typing import Any, Generic

from typing_extensions import TypeVar

_DT = TypeVar("_DT", default=str)  # decode type
_ET = TypeVar("_ET", default=Any)  # encode type


class AbstractSerializer(Generic[_DT, _ET]):
    """
    This class describes an abstract serializer.
    """

    def __init__(self, extensions: list[str] | None = None) -> None:
        super().__init__()
        self._extensions = (extensions or []).copy()

    def decode(self, s: _DT, **kwargs: Any) -> _ET:
        raise NotImplementedError()

    def encode(self, d: _ET, **kwargs: Any) -> _DT:
        raise NotImplementedError()

    def extensions(self) -> list[Any]:
        return self._extensions.copy()
