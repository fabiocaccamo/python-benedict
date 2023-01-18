import pathlib
import unittest

from benedict import benedict


class github_issue_0144_test_case(unittest.TestCase):
    """
    This class describes a github issue 0144 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/144

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0144
    """

    def test_init_with_pathlib_path_object_and_valid_path(self):
        # print(pathlib.Path("./test_issue_0144.json"))
        d = benedict(pathlib.Path("tests/github/test_issue_0144.json"), format="json")
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9})

    def test_init_with_pathlib_path_object_and_invalid_path(self):
        with self.assertRaises(ValueError):
            benedict(
                pathlib.Path("tests/github/test_issue_0144_invalid.json"), format="json"
            )
