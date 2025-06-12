from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qs, urlencode

from typing_extensions import override

from benedict.serializers.abstract import AbstractSerializer


class QueryStringSerializer(
    AbstractSerializer[str, dict[str, str] | dict[str, list[str]]]
):
    """
    This class describes a query-string serializer.
    """

    @override
    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "qs",
                "querystring",
            ],
        )

    @override
    def decode(  # type: ignore[override]
        self, s: str, flat: bool = True
    ) -> dict[str, str] | dict[str, list[str]]:
        qs_re = r"(?:([\w\-\%\+\.\|]+\=[\w\-\%\+\.\|]*)+(?:[\&]{1})?)+"
        qs_pattern = re.compile(qs_re)
        if qs_pattern.match(s):
            data = parse_qs(s)
            if flat:
                return {key: value[0] for key, value in data.items()}
            return data
        raise ValueError(f"Invalid query string: {s}")

    @override
    def encode(
        self, d: Mapping[str, str] | Mapping[str, list[str]], **kwargs: Any
    ) -> str:
        data = urlencode(d, **kwargs)
        return data
