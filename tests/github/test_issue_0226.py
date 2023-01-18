import unittest

import fsutil

from benedict import benedict


class github_issue_0226_test_case(unittest.TestCase):
    """
    This class describes a github issue 0226 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/226

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0226
    """

    def test_file_not_found_error_if_filepath_is_just_filename(self):
        b = benedict({"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9})
        filepath = "test.yml"
        b.to_yaml(filepath=filepath)
        self.assertTrue(fsutil.is_file(filepath))
        fsutil.remove_file(filepath)
