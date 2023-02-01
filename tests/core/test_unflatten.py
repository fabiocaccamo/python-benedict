import unittest

from benedict.core import unflatten as _unflatten


class unflatten_test_case(unittest.TestCase):
    """
    This class describes an unflatten test case.
    """

    def test_unflatten(self):
        d = {
            "a": 1,
            "b_c": 2,
            "d_e": 3,
        }
        u = _unflatten(d)
        r = {
            "a": 1,
            "b": {
                "c": 2,
            },
            "d": {
                "e": 3,
            },
        }
        self.assertEqual(u, r)

    def test_unflatten_with_custom_separator(self):
        d = {
            "a": 1,
            "b|c": 2,
            "d|e": 3,
        }
        u = _unflatten(d, separator="#")
        self.assertEqual(u, d)
        u = _unflatten(d, separator="|")
        r = {
            "a": 1,
            "b": {
                "c": 2,
            },
            "d": {
                "e": 3,
            },
        }
        self.assertEqual(u, r)

    def test_unflatten_with_nested_dict(self):
        d = {
            "a": 1,
            "b_c": {
                "u_v": 2,
            },
            "d_e": {
                "x_y_z": 3,
            },
        }
        u = _unflatten(d)
        r = {
            "a": 1,
            "b": {
                "c": {
                    "u": {
                        "v": 2,
                    },
                },
            },
            "d": {
                "e": {
                    "x": {
                        "y": {
                            "z": 3,
                        },
                    },
                },
            },
        }
        self.assertEqual(u, r)
