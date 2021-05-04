# -*- coding: utf-8 -*-

from benedict import benedict

import toml
import unittest


class github_issue_0053_test_case(unittest.TestCase):

    """
    https://github.com/fabiocaccamo/python-benedict/issues/53

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0053
    """
    def test_toml_dumps_valuerror_raised(self):

        toml_dummy = """
        [example.dummy]
        name = "dummy"
        """
        with self.assertRaises(ValueError):
            test = benedict(toml_dummy, format="toml")
            test["example.dummy.name"] = "new_dummy"
            toml.dumps(test)

    def test_toml_dumps_valuerror_not_raised(self):

        toml_dummy = """
        [example.dummy]
        name = "dummy"
        """
        raised = False
        try:
            test = benedict(toml_dummy, format="toml")
            test["example.dummy.name"] = "new_dummy"
            toml.dumps(test._dict)
        except ValueError:
            raised = True
        self.assertFalse(raised)
