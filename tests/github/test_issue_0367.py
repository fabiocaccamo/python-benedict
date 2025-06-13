import unittest

from benedict import benedict


class github_issue_0367_test_case(unittest.TestCase):
    """
    This class describes a github issue 0367 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/367

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0367
    """

    def test_dict_keys_with_separators_with_merge(self) -> None:
        d = {"foo.bar": 1}
        b = benedict()
        with self.assertRaises(ValueError):
            b.merge(d)
        # self.assertEqual(b, {"foo": {"bar": 1}})

    def test_dict_keys_with_separators_with_nested_merge(self) -> None:
        d = {"baz": {"foo.bar": 1}}
        b = benedict()
        with self.assertRaises(ValueError):
            b.merge(d)
        # self.assertEqual(b, {"baz": {"foo.bar": 1}})

    def test_dict_keys_with_separators_with_constructor(self) -> None:
        d = {"foo.bar": 1}
        with self.assertRaises(ValueError):
            benedict(d)
        # self.assertEqual(b, {"foo": {"bar": 1}})
