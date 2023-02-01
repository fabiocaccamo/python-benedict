import unittest

from benedict.core import clone as _clone
from benedict.core import traverse as _traverse


class traverse_test_case(unittest.TestCase):
    """
    This class describes a traverse test case.
    """

    def test_traverse(self):
        i = {
            "a": {
                "x": 2,
                "y": 3,
                "z": {
                    "ok": 5,
                },
            },
            "b": {
                "x": 7,
                "y": 11,
                "z": {
                    "ok": 13,
                },
            },
            "c": {
                "x": 17,
                "y": 19,
                "z": {
                    "ok": 23,
                },
            },
        }
        o = _clone(i)
        with self.assertRaises(ValueError):
            _traverse(o, True)

        def f(parent, key, value):
            if not isinstance(value, dict):
                parent[key] = value + 1

        _traverse(o, f)
        r = {
            "a": {
                "x": 3,
                "y": 4,
                "z": {
                    "ok": 6,
                },
            },
            "b": {
                "x": 8,
                "y": 12,
                "z": {
                    "ok": 14,
                },
            },
            "c": {
                "x": 18,
                "y": 20,
                "z": {
                    "ok": 24,
                },
            },
        }
        self.assertEqual(o, r)
