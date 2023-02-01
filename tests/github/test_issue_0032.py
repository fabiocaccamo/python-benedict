import unittest

from benedict import benedict


class github_issue_0032_test_case(unittest.TestCase):
    """
    This class describes a github issue 0032 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/32

    To run this specific test:
    - For each method comment @unittest.skip decorator
    - Run python -m unittest tests.github.test_issue_0032
    """

    @staticmethod
    def load_dict():
        return {
            "a": {
                "b": {
                    "c": {
                        "d": 10,
                    },
                    "x": 100,
                }
            }
        }

    def test_pointers_with_dict(self):
        b = benedict(self.load_dict())
        ab = benedict(b["a.b"])
        ab["c"]["d"] = 20
        ab["x"] = 200
        r = {
            "a": {
                "b": {
                    "c": {
                        "d": 20,
                    },
                    "x": 200,
                }
            }
        }
        self.assertEqual(b, r)
