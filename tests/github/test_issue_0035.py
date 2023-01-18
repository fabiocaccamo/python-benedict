import unittest

from benedict import benedict


class github_issue_0035_test_case(unittest.TestCase):
    """
    This class describes a github issue 0035 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/35

    To run this specific test:
    - For each method comment @unittest.skip decorator
    - Run python -m unittest tests.github.test_issue_0035
    """

    def test_keypath_separator_inheritance(self):
        b = benedict({"a.b": 1}, keypath_separator=None)
        c = benedict(b, keypath_separator=None)
        self.assertEqual(c.keypath_separator, None)
