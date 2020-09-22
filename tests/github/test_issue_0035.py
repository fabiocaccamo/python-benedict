# -*- coding: utf-8 -*-

from benedict import benedict

import unittest


class github_issue_0035_test_case(unittest.TestCase):

    """
    https://github.com/fabiocaccamo/python-benedict/issues/35

    To run this specific test:
    - For each method comment @unittest.skip decorator
    - Run python -m unittest tests.github.test_issue_0035
    """

    def test_pointers_with_dict(self):
        b = benedict({ 'a.b':1 }, keypath_separator=None)
        c = benedict(b, keypath_separator=None)
        self.assertEqual(c.keypath_separator, None)
