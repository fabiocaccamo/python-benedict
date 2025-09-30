from __future__ import annotations

import json

# fix benedict json dumps support - #57 #59 #61
from json import encoder
from typing import Any

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util


class JSONSerializer(AbstractSerializer[str, Any]):
    """
    This class describes a json serializer.
    """

    @staticmethod
    def disable_c_make_encoder() -> None:
        encoder.c_make_encoder = None  # type: ignore[attr-defined]

    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "json",
            ],
        )

    def decode(self, s: str, **kwargs: Any) -> Any:
        data = json.loads(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        kwargs.setdefault("default", self._encode_default)
        data = json.dumps(d, **kwargs)
        return data

    def _encode_default(self, obj: Any) -> list[Any] | str:
        if type_util.is_set(obj):
            return list(obj)
        elif type_util.is_datetime(obj):
            return obj.isoformat()
        elif type_util.is_decimal(obj):
            return str(obj)
        return str(obj)
