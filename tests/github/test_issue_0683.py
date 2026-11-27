import unittest

from benedict import benedict


class github_issue_0683_test_case(unittest.TestCase):
    """
    This class describes a github issue 0683 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/683

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0683
    """

    def test_stored_bracket_key_is_reachable(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d["rows[0]"], "a")
        self.assertEqual(d.get("rows[0]"), "a")
        self.assertIn("rows[0]", d)
        self.assertEqual(dict(d), {"rows[0]": "a", "keep": 1})
        self.assertEqual(d.flatten(), {"rows[0]": "a", "keep": 1})
        self.assertEqual(d.setdefault("rows[0]", "b"), "a")
        d["rows[0]"] = "b"
        self.assertEqual(d.pop("rows[0]"), "b")
        self.assertEqual(dict(d), {"keep": 1})

    def test_stored_bracket_key_is_reachable_without_keypath_separator(self) -> None:
        # index notation is parsed even when the keypath separator is disabled.
        d = benedict({"rows[0]": "a", "keep": 1}, keypath_separator=None)
        self.assertEqual(d["rows[0]"], "a")
        self.assertIn("rows[0]", d)
        del d["rows[0]"]
        self.assertEqual(dict(d), {"keep": 1})

    def test_keypath_syntax_still_works_when_key_is_not_stored(self) -> None:
        d = benedict({"rows": [1, 2], "keep": 1})
        self.assertEqual(d["rows[0]"], 1)
        self.assertEqual(d.get("rows[1]"), 2)
        self.assertIn("rows[0]", d)
        del d["rows[0]"]
        self.assertEqual(d["rows"], [2])

    def test_stored_key_takes_precedence_over_keypath(self) -> None:
        d = benedict({"rows": [1, 2], "rows[0]": "a"})
        self.assertEqual(d["rows[0]"], "a")
        d["rows[0]"] = "b"
        self.assertEqual(d["rows"], [1, 2])
        self.assertEqual(dict.__getitem__(d.dict(), "rows[0]"), "b")
