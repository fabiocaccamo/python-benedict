import unittest

from benedict import benedict


class github_issue_0592_test_case(unittest.TestCase):
    """
    This class describes a github issue 0592 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/592

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0592
    """

    def test_assigning_dict_to_its_own_nested_descendant_does_not_raise(self) -> None:
        # not self-referential yet at assignment time, so it must keep working
        d = benedict(keyattr_enabled=True, keyattr_dynamic=True)
        d.a.b.c = d
        self.assertIs(dict.__getitem__(d, "a")["b"]["c"], d)

    def test_assigning_dict_to_its_own_nested_descendant_twice_does_not_recurse(
        self,
    ) -> None:
        # once `d` contains itself, unwrapping it again must not raise
        # RecursionError (it used to crash the process)
        d = benedict(keyattr_enabled=True, keyattr_dynamic=True)
        d.a.b.c = d
        with self.assertRaises(ValueError):
            d.a.b.d.e = d

    def test_self_assignment_at_new_key_still_works(self) -> None:
        # assigning a dict to itself under a new key is unaffected by the fix
        d = benedict({"a": {"b": 1}})
        d["self"] = d
        self.assertIsInstance(d["self"], benedict)
        self.assertEqual(d["self"]["a"], {"b": 1})

    def test_normal_nested_dict_assignment_is_unaffected(self) -> None:
        # non self-referential values must still be unwrapped as before
        inner = benedict({"x": 1})
        outer = benedict()
        outer["inner"] = inner
        self.assertEqual(outer, {"inner": {"x": 1}})
        self.assertIsNot(outer["inner"], inner)
