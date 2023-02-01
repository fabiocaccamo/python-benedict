import unittest

from benedict import benedict


class github_issue_0088_test_case(unittest.TestCase):
    """
    This class describes a github issue 0088 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/88

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0088
    """

    def test_flatten_without_keypath_separator(self):
        d = benedict({"a": {"b": {"c": 1}}}, keypath_separator=None)
        f = d.flatten(".")
        self.assertEqual(f, {"a.b.c": 1})

    def test_flatten_with_separator_equal_to_keypath_separator(self):
        d = benedict({"a": {"b": {"c": 1}}}, keypath_separator=".")
        with self.assertRaises(ValueError):
            f = d.flatten(".")
        d = benedict({"a": {"b": {"c": 1}}}, keypath_separator="_")
        with self.assertRaises(ValueError):
            f = d.flatten("_")

    def test_flatten_with_separator_different_from_keypath_separator(self):
        d = benedict({"a": {"b": {"c": 1}}}, keypath_separator="_")
        f = d.flatten(".")
        self.assertEqual(f, {"a.b.c": 1})
        d = benedict({"a": {"b": {"c": 1}}}, keypath_separator=".")
        f = d.flatten("_")
        self.assertEqual(f, {"a_b_c": 1})
