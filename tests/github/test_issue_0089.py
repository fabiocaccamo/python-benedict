import unittest

from benedict import benedict


class github_issue_0089_test_case(unittest.TestCase):
    """
    This class describes a github issue 0089 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/89

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0089
    """

    def test_broken_serialization_with_benedict_attributes(self):
        d1 = benedict()
        d1["a"] = benedict({"b": 2})
        yaml_str = d1.to_yaml()
        # print(yaml_str)
        self.assertEqual(yaml_str, "a:\n  b: 2\n")
        d2 = benedict.from_yaml(yaml_str)
        self.assertEqual(d1, d2)
