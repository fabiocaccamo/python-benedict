import json
import unittest

from benedict import benedict


class github_issue_0048_test_case(unittest.TestCase):
    """
    This class describes a github issue 0048 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/48

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0048
    """

    def test_json_dumps_with_cloned_instance(self):
        test = benedict(
            {
                "foo": {
                    "bar": {
                        "foobar": {
                            "barbar": ["test"],
                        },
                    },
                },
            }
        )
        test2 = {
            "foo": {
                "bar": {
                    "foobar": {
                        "barbar": ["test2"],
                    },
                },
            },
        }
        test.merge(test2, overwrite=True, concat=True)
        # print(test.dump())
        self.assertEqual(
            test,
            {
                "foo": {
                    "bar": {
                        "foobar": {
                            "barbar": ["test", "test2"],
                        },
                    },
                },
            },
        )
