import pathlib
import unittest

from benedict import benedict


class github_issue_0355_test_case(unittest.TestCase):
    """
    This class describes a github issue 0355 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/355

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0355
    """

    def test_from_xls_with_options(self):
        # print(pathlib.Path("./test_issue_0144.json"))
        filepath = pathlib.Path("tests/github/test_issue_0355.xlsx")

        d = benedict.from_xls(filepath)
        # print(d.dump())
        self.assertEqual(
            d,
            {
                "values": [
                    {
                        "formula": '="A2 value is: "&A2',
                        "integer": 123,
                        "text": "abc",
                    }
                ]
            },
        )

        d = benedict.from_xls(filepath, data_only=True)
        # print(d.dump())
        self.assertEqual(
            d,
            {
                "values": [
                    {
                        "formula": "A2 value is: abc",
                        "integer": 123,
                        "text": "abc",
                    }
                ]
            },
        )
