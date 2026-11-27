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
        - Regular keys (no brackets) always return a scalar string value;
          the *flat* parameter on :meth:`decode` does not affect them.
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
            # keep_blank_values=True: the pair_re above already accepts empty
            # values ("a="), so keep them instead of silently dropping the key.
            data = parse_qs(s, keep_blank_values=True)
            return self._parse_bracket_notation(data)
        raise ValueError(f"Invalid query string: {s}")

    @staticmethod
    def _is_scalar(value: Any) -> bool:
        """Return True if the value can be represented as a query-string
        single value (any type that is not a sequence/mapping)."""
        return not isinstance(value, (Mapping, list, tuple, set, frozenset))

    @staticmethod
    def _is_plain_key(key: Any) -> bool:
        """Return True if the bracket notation can be appended to the key
        (a non-empty string that does not contain brackets already)."""
        return isinstance(key, str) and bool(key) and "[" not in key and "]" not in key

    @classmethod
    def _encode_array_pairs(
        cls, key: str, value: list[Any] | tuple[Any, ...]
    ) -> list[tuple[str, Any]] | None:
        """Encode a list value as repeated array-style pairs ("a[]=1&a[]=2").

        Return None when the value cannot be expressed with this notation
        (empty sequences, or sequences containing other sequences/mappings),
        so the caller can fall back to the previous behaviour.
        """
        if not value or not all(cls._is_scalar(item) for item in value):
            return None
        return [(f"{key}[]", item) for item in value]

    @classmethod
    def _encode_nested_pairs(
        cls, key: str, value: Mapping[str, Any]
    ) -> list[tuple[str, Any]] | None:
        """Encode a one-level dict value as bracketed pairs
        ("user[name]=joe&user[age]=42").

        Sub-values can also be sequences with more than one item
        ("user[tags]=a&user[tags]=b"), the notation the decoder turns
        back into a list.
        Return None when the value cannot be expressed with this notation
        (empty mappings, bracketed/empty/non-string sub-keys, or unrepresentable
        sub-values), so the caller can fall back to the previous behaviour.
        """
        pairs: list[tuple[str, Any]] = []
        for sub_key, sub_value in value.items():
            if not cls._is_plain_key(sub_key):
                return None
            if cls._is_scalar(sub_value):
                pairs.append((f"{key}[{sub_key}]", sub_value))
                continue
            if (
                isinstance(sub_value, (list, tuple))
                and len(sub_value) > 1
                and all(cls._is_scalar(item) for item in sub_value)
            ):
                pairs.extend((f"{key}[{sub_key}]", item) for item in sub_value)
                continue
            return None
        return pairs or None

    @classmethod
    def _encode_bracket_notation(cls, data: Mapping[str, Any]) -> list[tuple[str, Any]]:
        """Convert a mapping into key/value pairs using the bracket notation
        supported by :meth:`decode` (its inverse operation):

        - ``{"a": ["1", "2"]}``       → ``[("a[]", "1"), ("a[]", "2")]``
        - ``{"user": {"name": "joe"}}`` → ``[("user[name]", "joe")]``

        Values that cannot be expressed with this notation are kept
        as they are, preserving the previous behaviour.
        """
        pairs: list[tuple[str, Any]] = []
        for key, value in data.items():
            pair_values: list[tuple[str, Any]] | None = None
            if cls._is_plain_key(key):
                if isinstance(value, (list, tuple)):
                    pair_values = cls._encode_array_pairs(key, value)
                elif isinstance(value, Mapping):
                    pair_values = cls._encode_nested_pairs(key, value)
            if pair_values is None:
                pairs.append((key, value))
            else:
                pairs.extend(pair_values)
        return pairs

    @override
    def encode(self, d: Mapping[str, Any], **kwargs: Any) -> str:
        data = self._encode_bracket_notation(d)
        # keep the bracket characters literal in keys ("a[]=1") so the
        # output matches the array-style/bracketed notation accepted by
        # decode, instead of its percent-encoded form ("a%5B%5D=1").
        kwargs.setdefault("safe", "[]")
        return urlencode(data, **kwargs)
