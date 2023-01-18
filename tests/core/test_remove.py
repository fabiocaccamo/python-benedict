import unittest

from benedict.core import remove as _remove


class remove_test_case(unittest.TestCase):
    """
    This class describes a remove test case.
    """

    def test_remove_with_single_key(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        _remove(d, "c")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_args(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        _remove(d, "c", "d", "e")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_list(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        _remove(d, ["c", "d", "e"])
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)
