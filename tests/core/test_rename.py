import unittest

from benedict.core import rename as _rename


class rename_test_case(unittest.TestCase):
    """
    This class describes a rename test case.
    """

    def test_rename(self):
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
        _rename(d, "a", "d")
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

    def test_rename_with_same_key(self):
        d = {
            "a": 1,
            "b": 2,
        }
        _rename(d, "a", "a")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_rename_to_existing_name(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        with self.assertRaises(KeyError):
            _rename(d, "a", "c")
