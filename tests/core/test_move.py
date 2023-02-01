import unittest

from benedict.core import move as _move


class move_test_case(unittest.TestCase):
    """
    This class describes a move test case.
    """

    def test_move(self):
        d = {
            "a": {
                "x": 1,
                "y": 1,
            },
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 3,
                "y": 3,
            },
        }
        _move(d, "a", "d")
        r = {
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 3,
                "y": 3,
            },
            "d": {
                "x": 1,
                "y": 1,
            },
        }
        self.assertEqual(d, r)

    def test_move_with_same_key(self):
        d = {
            "a": 1,
            "b": 2,
        }
        _move(d, "a", "a")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)
