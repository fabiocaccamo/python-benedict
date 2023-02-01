import re
import unittest

from benedict.core import match as _match


class match_test_case(unittest.TestCase):
    """
    This class describes a match test case.
    """

    @staticmethod
    def _get_dict():
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

    def test_match_with_string_pattern(self):
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

    def test_match_with_regex_pattern(self):
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

    def test_match_with_invalid_pattern(self):
        d = self._get_dict()
        with self.assertRaises(ValueError):
            values = _match(d, 100)
