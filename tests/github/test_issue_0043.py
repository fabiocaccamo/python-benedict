import unittest

import yaml

from benedict import benedict


class github_issue_0043_test_case(unittest.TestCase):
    """
    This class describes a github issue 0043 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/43

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0043
    """

    def test_to_yaml(self):
        b = benedict({"level1": {"level2": "Hello world"}})
        s = b.to_yaml()
        r = """level1:
  level2: Hello world
"""
        self.assertEqual(s, r)

    def test_dict_compatibility(self):
        yaml.safe_dump(dict(benedict({})))
        yaml.safe_dump(dict(benedict({"level1": None})))
        yaml.safe_dump(dict(benedict({"level1": {"level2": "blablabla"}})))
