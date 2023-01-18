import json
import unittest

from benedict import benedict


class github_issue_0057_test_case(unittest.TestCase):
    """
    This class describes a github issue 0057 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/57

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0057
    """

    def test_json_dump_with_initial_empty_dict_reference(self):
        r = {}
        d = benedict(r)
        d["a"] = 1
        self.assertEqual(d, {"a": 1})
        self.assertEqual(d.to_json(), '{"a": 1}')
        self.assertEqual(json.dumps(d.dict()), '{"a": 1}')
        self.assertEqual(json.dumps(d), '{"a": 1}')
