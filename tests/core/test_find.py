import unittest

from benedict.core import find as _find


class find_test_case(unittest.TestCase):
    """
    This class describes a find test case.
    """

    def test_find_with_single_result(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": None,
        }
        o = _find(i, ["x", "y", "b", "z"], 5)
        self.assertEqual(o, 2)

    def test_find_with_multiple_results(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": None,
        }
        o = _find(i, ["a", "x", "b", "y"])
        self.assertEqual(o, 1)

    def test_find_with_no_result(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": None,
        }
        o = _find(i, ["x", "y", "z"])
        self.assertEqual(o, None)

    def test_find_with_no_result_and_default(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": None,
        }
        o = _find(i, ["x", "y", "z"], 5)
        self.assertEqual(o, 5)
