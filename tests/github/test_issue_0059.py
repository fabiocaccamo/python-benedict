import unittest

from benedict import benedict


class github_issue_0059_test_case(unittest.TestCase):
    """
    This class describes a github issue 0059 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/59

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0059
    """

    def test_init_with_empty_dict_then_merge_with_dict_should_affect_both_dicts(self):
        initial_empty_dict = {}
        the_benedict = benedict(initial_empty_dict)
        the_benedict.merge({"foo": "bar"})
        self.assertEqual(initial_empty_dict, {"foo": "bar"})
        self.assertEqual(the_benedict, {"foo": "bar"})

    def test_init_empty_dict_then_assign_another_empty_dict_as_first_key_should_work(
        self,
    ):
        d = benedict()
        # these two lines are inefficient
        # d["a"] = {"b": {}} is better. Regardless, will test both
        d["a"] = {}
        d["a"]["b"] = {}
        self.assertEqual(d, {"a": {"b": {}}})

        d2 = benedict()
        d2["a"] = {"b": {}}
        self.assertEqual(d2, {"a": {"b": {}}})
