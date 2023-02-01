import unittest

from benedict.core import flatten as _flatten


class flatten_test_case(unittest.TestCase):
    """
    This class describes a flatten test case.
    """

    def test_flatten(self):
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": {
                    "e": 3,
                    "f": 4,
                    "g": {
                        "h": 5,
                    },
                }
            },
        }
        o = _flatten(i)
        r = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_custom_separator(self):
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": {
                    "e": 3,
                    "f": 4,
                    "g": {
                        "h": 5,
                    },
                }
            },
        }
        o = _flatten(i, separator="/")
        r = {
            "a": 1,
            "b": 2,
            "c/d/e": 3,
            "c/d/f": 4,
            "c/d/g/h": 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_key_conflict(self):
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": 3,
            },
            "c_d": 4,
            "d_e": 5,
            "d": {
                "e": 6,
            },
        }
        with self.assertRaises(KeyError):
            o = _flatten(i)
        # r = {
        #     'a': 1,
        #     'b': 2,
        #     'c_d': 4,
        #     'd_e': 5,
        # }
        # self.assertEqual(o, r)
