import unittest

from benedict import benedict


class github_issue_0294_test_case(unittest.TestCase):
    """
    This class describes a github issue 0294 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/294

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0294
    """

    def test_assigning_benedict_element_to_itself_clears_the_element(self) -> None:
        d = benedict({"a": {"b": 1}})
        d["a"] = d["a"]
        self.assertEqual(d, {"a": {"b": 1}})
        d.a = d.a
        self.assertEqual(d, {"a": {"b": 1}})
