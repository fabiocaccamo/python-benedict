import unittest
from benedict import benedict


class github_issue_0432_test_case(unittest.TestCase):
    """
    This class describes a github issue 0432 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/432

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0432
    """

    def test_tuple_as_key_like_dict_432(self):
        d1 = {}
        d2 = benedict()
        d1[(0, 0, 1)] = "a"
        d2[(0, 0, 1)] = "a"
        self.assertEqual(d1, d2)

    def test_tuple_as_key_like_dict_412(self):
        d = {}
        d[("a", True)] = "test"

        b1 = benedict()
        b1[("a", True)] = "test"
        self.assertEqual(d, b1)

        b2 = benedict()
        b2.update({("a", True): "test"})
        self.assertEqual(d, b2)
