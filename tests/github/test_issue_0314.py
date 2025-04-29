import unittest

import yaml

from benedict import benedict


class github_issue_0314_test_case(unittest.TestCase):
    """
    This class describes a github issue 0314 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/294

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0314
    """

    def test_yaml_serializer_produces_inconsistent_results(self) -> None:
        b = benedict({"foo": "foo"})
        b["hello.world"] = "hello world"

        # output as custom object using yaml manually
        # print(yaml.dump({"world": dict(b)}))

        # output as custom object using yaml manually
        # print(yaml.dump({"world": b}))

        # output as normal dict using yaml manually
        # print(yaml.dump({"world": b.dict()}))

        # output as normal dict using benedict yaml serializer
        # print(benedict({"world": b}).to_yaml())

        self.assertEqual(
            yaml.dump({"world": b.dict()}),
            benedict({"world": b}).to_yaml(),
        )
