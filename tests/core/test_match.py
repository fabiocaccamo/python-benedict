from __future__ import annotations

import re
import unittest

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

    def test_match_with_invalid_pattern(self) -> None:
        d = self._get_dict()
        with self.assertRaises(ValueError):
            _ = _match(d, 100)  # type: ignore[arg-type]
