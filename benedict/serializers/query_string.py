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

    @staticmethod
    def _parse_bracket_notation(
        data: dict[str, list[str]],
    ) -> dict[str, Any]:
        """Convert parse_qs output into nested dicts / lists for bracket keys.

        - ``a[]=1&a[]=2``       → ``{"a": ["1", "2"]}``
        - ``user[name]=joe``    → ``{"user": {"name": "joe"}}``
        - Regular keys always return a scalar string value.
        """
        _array_re = re.compile(r"^([^\[]+)\[\]$")
        _nested_re = re.compile(r"^([^\[]+)\[([^\]]+)\]$")
        result: dict[str, Any] = {}
        for key, values in data.items():
            m_array = _array_re.match(key)
            m_nested = _nested_re.match(key)
            if m_array:
                base = m_array.group(1)
                result[base] = values
            elif m_nested:
                parent, child = m_nested.group(1), m_nested.group(2)
                if parent not in result or not isinstance(result[parent], dict):
                    result[parent] = {}
                result[parent][child] = values[0] if len(values) == 1 else values
            else:
                result[key] = values[0]
        return result

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
        # Allow exactly one trailing empty segment (trailing "&" is valid)
        if pairs and not pairs[-1]:
            pairs = pairs[:-1]
        if all(pair_re.match(pair) for pair in pairs):
            data = parse_qs(s)
            return self._parse_bracket_notation(data)
        raise ValueError(f"Invalid query string: {s}")

    @override
    def encode(
        self, d: Mapping[str, str] | Mapping[str, list[str]], **kwargs: Any
    ) -> str:
        data = urlencode(d, **kwargs)
        return data
