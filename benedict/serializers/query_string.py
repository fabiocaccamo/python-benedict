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
        # A query string is a sequence of "key=value" pairs joined by "&".
        # Each key must be non-empty and free of whitespace, "=" and "&";
        # each value must be free of whitespace and "&" (spaces are encoded
        # as "+" or "%20"). This accepts real-world keys such as array-style
        # "a[]" / "user[name]" while still rejecting other formats (TOML, YAML,
        # JSON, XML), plain text and URLs.
        pair_re = re.compile(r"^[^\s=&]+=[^\s&]*$")
        pairs = s.split("&")
        if all(pair_re.match(pair) for pair in pairs):
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
