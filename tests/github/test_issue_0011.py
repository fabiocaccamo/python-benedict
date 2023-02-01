import unittest

from benedict import benedict


class github_issue_0011_test_case(unittest.TestCase):
    """
    This class describes a github issue 0011 test case.
    """

    def test_github_issue_0011(self):
        """
        https://github.com/fabiocaccamo/python-benedict/issues/11
        """
        d = {
            "lorem": [
                {"ipsum": "a"},
                {"ipsum": "b"},
                {"not_ipsum": "c"},
            ],
            "nested": [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
            ],
        }
        b = benedict(d)

        v = b.match("lorem[*].ipsum", indexes=True)
        v.sort()
        self.assertEqual(v, ["a", "b"])

        v = b.match("nested[*][*]", indexes=True)
        v.sort()
        self.assertEqual(v, [1, 2, 3, 4, 5, 6, 7, 8, 9])
