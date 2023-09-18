import unittest

from benedict import benedict


class github_issue_0334_test_case(unittest.TestCase):
    """
    This class describes a github issue 0334 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/294

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0334
    """

    def test_union_with_assignement_operator(self):
        a = {"a": "a", "b": "b"}
        b = {"b": "b", "c": "c"}

        ab = benedict(a.copy())
        bb = benedict(b.copy())
        self.assertEqual(a | b, ab | bb)

        a |= b.copy()
        ab |= bb.copy()
        self.assertEqual(a, ab)
