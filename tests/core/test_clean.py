import unittest

from benedict.core import clean as _clean


class clean_test_case(unittest.TestCase):
    """
    This class describes a clean test case.
    """

    def test_clean(self):
        i = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "g": None,
            "h": "0",
        }

        o = i.copy()
        _clean(o)
        r = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }
        self.assertEqual(o, r)

        o = i.copy()
        _clean(o, collections=False)
        r = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }
        self.assertEqual(o, r)

        o = i.copy()
        _clean(o, strings=False)
        r = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "h": "0",
        }
        self.assertEqual(o, r)
