import unittest

from benedict import benedict


class github_issue_0284_test_case(unittest.TestCase):
    """
    This class describes a github issue 0284 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/284

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0284
    """

    def test_from_ini_returns_str_instead_of_dict(self) -> None:
        original = benedict(
            {
                "section1": {
                    "key1": "value1",
                },
                "sectionA": {
                    "keyA": "valueA",
                    "keyB": "valueB",
                    "keyC": {
                        "subkeyC": "subvalueC",
                    },
                },
            }
        )
        readback = benedict.from_ini(original.to_ini())
        keypath = "sectionA.keyC"
        # print("original vs readback")
        # print(original.get(keypath), type(original.get(keypath)))
        # print("-- vs --")
        # print(readback.get(keypath), type(readback.get(keypath)))
        self.assertEqual(original.get(keypath), readback.get(keypath))
