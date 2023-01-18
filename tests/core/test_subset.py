import unittest

from benedict.core import subset as _subset


class subset_test_case(unittest.TestCase):
    """
    This class describes a subset test case.
    """

    def test_subset_with_keys_as_args(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        o = _subset(i, "c", "f", "x")
        r = {
            "c": 3,
            "f": 6,
            "x": None,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_subset_with_keys_as_list(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        o = _subset(i, ["c", "f", "x"])
        r = {
            "c": 3,
            "f": 6,
            "x": None,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)
