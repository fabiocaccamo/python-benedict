# import toml
import unittest

from benedict import benedict


class github_issue_0110_test_case(unittest.TestCase):
    """
    This class describes a github issue 0110 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/110

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0110
    """

    def test_toml_circular_reference_detected(self):
        d = {"a": {"b": {"c": 1}}}
        d["e"] = benedict({"f": 2})

        b = benedict()
        b.update(d)
        # b.merge(d)

        t = b.to_toml()
        # print(t)
