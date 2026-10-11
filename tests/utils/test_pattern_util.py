from __future__ import annotations

import time
import unittest

from benedict.utils import pattern_util


class pattern_util_test_case(unittest.TestCase):
    """
    This class describes a pattern utility test case.
    """

    def _matches(self, pattern: str, s: str) -> bool:
        return bool(pattern_util.compile_wildcard_pattern(pattern).match(s))

    def test_compile_wildcard_pattern_without_wildcards(self) -> None:
        self.assertTrue(self._matches("abc", "abc"))
        self.assertFalse(self._matches("abc", "abcd"))
        self.assertFalse(self._matches("abc", "xabc"))
        self.assertFalse(self._matches("abc", "abc\n"))
        self.assertTrue(self._matches("", ""))
        self.assertFalse(self._matches("", "a"))

    def test_compile_wildcard_pattern_with_wildcards(self) -> None:
        self.assertTrue(self._matches("*", ""))
        self.assertTrue(self._matches("*", "anything\nat all"))
        self.assertTrue(self._matches("a*", "abc"))
        self.assertTrue(self._matches("*c", "abc"))
        self.assertTrue(self._matches("a*c", "ac"))
        self.assertTrue(self._matches("a*b*c", "a-b-b-c"))
        self.assertFalse(self._matches("a*b*c", "a-c-b"))
        self.assertTrue(self._matches("a**c", "abc"))

    def test_compile_wildcard_pattern_matches_special_chars_literally(self) -> None:
        self.assertTrue(self._matches("a.b", "a.b"))
        self.assertFalse(self._matches("a.b", "aXb"))
        self.assertFalse(self._matches("a+b", "aab"))
        self.assertTrue(self._matches("items[0]", "items[0]"))
        self.assertTrue(self._matches("items[*].x", "items[12].x"))
        self.assertTrue(self._matches("f(1)|?$^", "f(1)|?$^"))

    def test_compile_wildcard_pattern_without_catastrophic_backtracking(
        self,
    ) -> None:
        s = "a" * 2000
        start = time.monotonic()
        self.assertFalse(self._matches("*" * 30 + "z", s))
        self.assertFalse(self._matches("*a" * 30 + "z", s))
        self.assertTrue(self._matches("*a" * 30, s))
        self.assertLess(time.monotonic() - start, 1)
