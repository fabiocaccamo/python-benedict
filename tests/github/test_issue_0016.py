import unittest

from benedict import benedict


class github_issue_0016_test_case(unittest.TestCase):
    """
    This class describes a github issue 0016 test case.
    """

    def test_github_issue_0016(self):
        """
        https://github.com/fabiocaccamo/python-benedict/issues/16
        """
        d = {
            "components": [
                {
                    "name": "comp1",
                    "value": "value1",
                    "subcomponent": {
                        "name": "subcomp1",
                    },
                },
                {
                    "name": "comp2",
                    "value": "value2",
                    "subcomponent": {
                        "name": "subcomp2",
                    },
                },
                {
                    "name": "comp3",
                    "value": "value3",
                    "subcomponent": {
                        "name": "subcomp3",
                    },
                },
            ],
        }
        b = benedict(d)
        v = b.match("components[*].subcomponent.name")
        self.assertEqual(v, ["subcomp1", "subcomp2", "subcomp3"])
