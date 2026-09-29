from __future__ import annotations

import unittest
from typing import Any

from benedict.core import clean as _clean


class clean_test_case(unittest.TestCase):
    """
    This class describes a clean test case.
    """

    def test_clean_nested_tuple_values(self) -> None:
        nested = {"keep": 1, "drop": None}
        data = {"items": (nested, (None, 2), {None, 3}, ["", 4], (None,), 0, False)}
        _clean(data)
        self.assertEqual(data, {"items": ({"keep": 1}, (2,), {3}, [4], 0, False)})
        self.assertEqual(nested, {"keep": 1, "drop": None})

    def test_clean_nested_set_values(self) -> None:
        data = {"items": {(None, 1), (" ", 2), (None,), (3, (None, 4))}}
        _clean(data)
        self.assertEqual(data, {"items": {(1,), (2,), (3, (4,))}})

    def test_clean_nested_tuple_options(self) -> None:
        data = {"items": (None, "", (" ", None))}
        _clean(data, strings=False)
        self.assertEqual(data, {"items": ("", (" ",))})

        data = {"items": (None, "", (" ", None))}
        _clean(data, collections=False)
        self.assertEqual(data, {"items": (None, "", (" ", None))})

    def test_clean(self) -> None:
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

    def test_clean_nested_dicts(self) -> None:
        # https://github.com/fabiocaccamo/python-benedict/issues/383
        d: dict[str, Any] = {
            "a": {
                "b": {
                    "c": {},
                },
            },
        }
        _clean(d, collections=True)
        r: dict[str, Any] = {}
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
