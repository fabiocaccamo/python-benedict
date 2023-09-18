import unittest

from benedict import benedict


class github_issue_0333_test_case(unittest.TestCase):
    """
    This class describes a github issue 0333 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/294

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0333
    """

    def test_items_value_type(self):
        likes = {
            "fruit": {
                "apple": "green",
                "banana": "yellow",
                "raspberry": "red",
            }
        }
        likes = benedict(
            likes,
            keyattr_enabled=True,
            keyattr_dynamic=False,
        )
        # print(type(likes.items()))
        # print(likes.items())
        for _, v in likes.items():
            self.assertEqual(type(v), benedict)

    def test_values_value_type(self):
        likes = {
            "fruit": {
                "apple": "green",
                "banana": "yellow",
                "raspberry": "red",
            }
        }
        likes = benedict(
            likes,
            keyattr_enabled=True,
            keyattr_dynamic=False,
        )
        # print(type(likes.values()))
        # print(likes.values())
        for v in likes.values():
            self.assertEqual(type(v), benedict)
