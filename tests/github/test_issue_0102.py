import json
import unittest

import orjson

from benedict import benedict


class github_issue_0102_test_case(unittest.TestCase):
    """
    This class describes a github issue 0102 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/102

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0102
    """

    def test_orjson_benedict_reference_with_setitem(self):
        d = benedict(
            {
                "internal": {"mykey": "OLD"},
            }
        )

        d["internal"] = benedict({"mykey": "NEW"})
        self.assertEqual(d["internal"], {"mykey": "NEW"})

        s = orjson.dumps(d)
        d = orjson.loads(s)

        self.assertEqual(d, {"internal": {"mykey": "NEW"}})

    def test_orjson_benedict_reference_with_contructor_and_setitem(self):
        d = benedict(
            {
                "internal": benedict({"mykey": "OLD"}),
            }
        )

        d["internal"] = benedict({"mykey": "NEW"})
        self.assertEqual(d["internal"], {"mykey": "NEW"})

        s = orjson.dumps(d)
        d = orjson.loads(s)

        self.assertEqual(d, {"internal": {"mykey": "NEW"}})

    def test_orjson_benedict_reference_with_contructor_and_nested_benedict_instances(
        self,
    ):
        d = benedict(
            {
                "a": benedict(
                    {
                        "b": benedict(
                            {
                                "c": benedict(
                                    {
                                        "d": "OLD",
                                    }
                                ),
                            }
                        ),
                    }
                ),
            }
        )

        d["a"]["b"]["c"] = benedict({"d": "NEW"})
        self.assertEqual(d["a"]["b"]["c"]["d"], "NEW")

        s = orjson.dumps(d)
        d = orjson.loads(s)

        self.assertEqual(d["a"]["b"]["c"], {"d": "NEW"})
