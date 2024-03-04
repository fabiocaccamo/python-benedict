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
            "i": (1, None, 2, 3, " "),
            "j": {1, None, 2, 3, " "},
        }

        o = i.copy()
        _clean(o)
        r = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
            "i": (1, 2, 3),
            "j": {1, 2, 3},
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
            "i": (1, None, 2, 3, " "),
            "j": {1, None, 2, 3, " "},
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
            "i": (1, 2, 3, " "),
            "j": {1, 2, 3, " "},
        }
        self.assertEqual(o, r)

    def test_clean_nested_dicts(self):
        # https://github.com/fabiocaccamo/python-benedict/issues/383
        d = {
            "a": {
                "b": {
                    "c": {},
                },
            },
        }
        _clean(d, collections=True)
        r = {}
        self.assertEqual(d, r)

        d = {
            "a": {
                "b": {
                    "c": {},
                },
                "d": 1,
            },
        }
        _clean(d, collections=True)
        r = {
            "a": {
                "d": 1,
            },
        }
        self.assertEqual(d, r)

        d = {
            "a": {
                "b": [
                    0,
                    1,
                    2,
                    3,
                    {},
                    {
                        "c": [None, 4, None, 5],
                    },
                ],
            },
        }
        _clean(d, collections=True)
        r = {
            "a": {
                "b": [
                    0,
                    1,
                    2,
                    3,
                    {
                        "c": [4, 5],
                    },
                ],
            },
        }
        self.assertEqual(d, r)

        d = {
            "a": {
                "b": [
                    (None, None, None),
                    (None, 1, 2),
                    {3, None, 4},
                    {5, 6, None},
                ],
                "c": (None, None),
                "d": {None},
            },
        }
        _clean(d, collections=True)
        r = {
            "a": {
                "b": [
                    (1, 2),
                    {3, 4},
                    {5, 6},
                ],
            },
        }
        self.assertEqual(d, r)
