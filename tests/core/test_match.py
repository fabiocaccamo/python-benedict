from __future__ import annotations

import re
import time
import unittest

from benedict import benedict
from benedict.core import match as _match


class match_test_case(unittest.TestCase):
    """
    This class describes a match test case.
    """

    @staticmethod
    def _get_dict() -> dict[str, str]:
        return {
            "DOC_0001.pdf": "DOC_0001.pdf",
            "IMG_0001.jpg": "IMG_0001.jpg",
            "IMG_0001.raw": "IMG_0001.raw",
            "DOC_0002.pdf": "DOC_0002.pdf",
            "IMG_0002.jpg": "IMG_0002.jpg",
            "IMG_0002.raw": "IMG_0002.raw",
            "DOC_0003.pdf": "DOC_0003.pdf",
            "IMG_0003.jpg": "IMG_0003.jpg",
            "IMG_0003.raw": "IMG_0003.raw",
            "DOC_0004.pdf": "DOC_0004.pdf",
            "IMG_0004.jpg": "IMG_0004.jpg",
            "IMG_0004.raw": "IMG_0004.raw",
            "DOC_0005.pdf": "DOC_0005.pdf",
            "IMG_0005.jpg": "IMG_0005.jpg",
            "IMG_0005.raw": "IMG_0005.raw",
        }

    def test_match_with_string_pattern(self) -> None:
        d = self._get_dict()
        values = _match(d, "IMG_*.jpg")
        values.sort()
        expected_values = [
            "IMG_0001.jpg",
            "IMG_0002.jpg",
            "IMG_0003.jpg",
            "IMG_0004.jpg",
            "IMG_0005.jpg",
        ]
        self.assertEqual(values, expected_values)

    def test_match_with_regex_pattern(self) -> None:
        d = self._get_dict()
        values = _match(d, re.compile(r"^DOC\_"))
        values.sort()
        expected_values = [
            "DOC_0001.pdf",
            "DOC_0002.pdf",
            "DOC_0003.pdf",
            "DOC_0004.pdf",
            "DOC_0005.pdf",
        ]
        self.assertEqual(values, expected_values)

    def test_match_with_suffix_wildcard(self) -> None:
        # Suffix wildcard like "*.jpg" must not match "IMG_0001.jpg.bak" –
        # i.e. the full keypath must be consumed, not just a prefix.
        d = {
            "IMG_0001.jpg": "IMG_0001.jpg",
            "IMG_0001.jpg.bak": "IMG_0001.jpg.bak",
            "DOC_0001.pdf": "DOC_0001.pdf",
        }
        values = _match(d, "*.jpg")
        self.assertEqual(values, ["IMG_0001.jpg"])

    def test_match_does_not_ignore_a_terminal_newline(self) -> None:
        d = {"key": 1, "key\n": 2, "key\nextra": 3}
        self.assertEqual(_match(d, "key"), [1])
        self.assertEqual(_match(d, "key*"), [1, 2, 3])
        self.assertEqual(_match(d, "key\n"), [2])
        self.assertEqual(_match(d, re.compile("key")), [1, 2, 3])

    def test_match_with_string_pattern_matches_special_chars_literally(self) -> None:
        d = {"aXb": 1, "a.b": 2, "aab": 3, "f(1)": 4, "x|y": 5}
        self.assertEqual(_match(d, "a.b"), [2])
        self.assertEqual(_match(d, "a+b"), [])
        self.assertEqual(_match(d, "f(1)"), [4])
        self.assertEqual(_match(d, "x|y"), [5])

    def test_match_with_string_pattern_and_consecutive_wildcards(self) -> None:
        d = self._get_dict()
        self.assertEqual(_match(d, "IMG_**.jpg"), _match(d, "IMG_*.jpg"))

    def test_match_with_string_pattern_without_catastrophic_backtracking(
        self,
    ) -> None:
        # these patterns used to take an exponential time
        d = {"a" * 2000: 1}
        start = time.monotonic()
        self.assertEqual(_match(d, "*" * 30 + "z"), [])
        self.assertEqual(_match(d, "*a" * 30 + "z"), [])
        self.assertEqual(_match(d, "*a" * 30), [1])
        self.assertLess(time.monotonic() - start, 1)

    def test_match_with_invalid_pattern(self) -> None:
        d = self._get_dict()
        with self.assertRaises(ValueError):
            _ = _match(d, 100)  # type: ignore[arg-type]

    def test_match_with_tuple_indexes(self) -> None:
        data = benedict({"items": ({"value": 1}, {"value": 2})})
        self.assertEqual(data["items[0].value"], 1)
        self.assertEqual(data.match("items[*].value"), [1, 2])

    def test_match_nested_plain_mappings(self) -> None:
        data = {"items": [{"value": 2}, {"value": 1}]}
        self.assertEqual(_match(data, "items[*].value"), [2, 1])
        self.assertEqual(_match(data, "items[*].value", indexes=False), [])

    def test_match_uses_original_keys_for_values(self) -> None:
        data = {2: "two", None: "none", "a.b": "literal", "a": {"b": "nested"}}
        self.assertEqual(
            _match(data, "*"), ["two", "none", {"b": "nested"}, "literal", "nested"]
        )
        self.assertEqual(benedict({2: "two"}).match("*"), ["two"])

    def test_match_custom_separator_and_tuple_indexes(self) -> None:
        data = {"rows": ({"name": "first"}, {"name": "second"})}
        self.assertEqual(
            _match(data, "rows[*]/name", separator="/"), ["first", "second"]
        )
        wrapped = benedict(data, keypath_separator="/")
        self.assertEqual(wrapped.match("rows[*]/name"), ["first", "second"])

    def test_match_literal_bracket_keys(self) -> None:
        self.assertEqual(_match({"item[0]": "literal"}, "item[0]"), ["literal"])
