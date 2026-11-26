import unittest

from benedict import benedict


class github_issue_0683_test_case(unittest.TestCase):
    """
    This class describes a github issue 0683 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/683

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0683
    """

    def test_getitem_returns_stored_bracket_key_value(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d["rows[0]"], "a")

    def test_get_returns_stored_bracket_key_value(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d.get("rows[0]"), "a")

    def test_contains_with_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertIn("rows[0]", d)

    def test_delitem_with_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        del d["rows[0]"]
        self.assertEqual(dict(d), {"keep": 1})

    def test_pop_with_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d.pop("rows[0]"), "a")
        self.assertEqual(dict(d), {"keep": 1})

    def test_setitem_overwrites_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        d["rows[0]"] = "b"
        self.assertEqual(dict(d), {"rows[0]": "b", "keep": 1})

    def test_setdefault_with_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d.setdefault("rows[0]", "b"), "a")
        self.assertEqual(dict(d), {"rows[0]": "a", "keep": 1})

    def test_dict_conversion_with_stored_bracket_key(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(dict(d), {"rows[0]": "a", "keep": 1})

    def test_flatten_keeps_stored_bracket_key_values(self) -> None:
        d = benedict({"rows[0]": "a", "keep": 1})
        self.assertEqual(d.flatten(), {"rows[0]": "a", "keep": 1})

    def test_keypath_syntax_still_works_when_key_is_not_stored(self) -> None:
        d = benedict({"rows": [1, 2], "keep": 1})
        self.assertEqual(d["rows[0]"], 1)
        self.assertEqual(d.get("rows[1]"), 2)
        self.assertIn("rows[0]", d)
        del d["rows[0]"]
        self.assertEqual(d["rows"], [2])

    def test_stored_key_takes_precedence_over_keypath(self) -> None:
        # when both a literal key and a keypath target exist,
        # the stored key wins.
        d = benedict({"rows": [1, 2], "rows[0]": "a"})
        self.assertEqual(d["rows[0]"], "a")
        d["rows[0]"] = "b"
        self.assertEqual(d["rows"], [1, 2])
        self.assertEqual(dict.__getitem__(d.dict(), "rows[0]"), "b")

    def test_dotted_stored_key_reachable_with_check_keys_disabled(self) -> None:
        # separator-containing keys cannot be created through the keypath API,
        # but when they are stored through raw dict access they must be
        # reachable too (stored key takes precedence).
        d = benedict(check_keys=False)
        dict.__setitem__(d, "a.b", 1)
        self.assertEqual(d["a.b"], 1)
        self.assertIn("a.b", d)
