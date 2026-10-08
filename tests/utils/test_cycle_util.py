from __future__ import annotations

import unittest

from benedict import benedict
from benedict.utils import cycle_util


class cycle_util_test_case(unittest.TestCase):
    """
    This class describes a cycle util test case.
    """

    def test_get_id(self) -> None:
        d = {"a": 1}
        self.assertEqual(cycle_util.get_id(d), id(d))

    def test_get_id_with_benedict_uses_wrapped_dict(self) -> None:
        d = {"a": {"b": 1}}
        b = benedict(d)
        # each access creates a new wrapper around the same nested dict
        self.assertIsNot(b["a"], b["a"])
        self.assertEqual(cycle_util.get_id(b["a"]), cycle_util.get_id(b["a"]))
        self.assertEqual(cycle_util.get_id(b["a"]), id(d["a"]))

    def test_visit(self) -> None:
        path_ids: set[int] = set()
        d = {"a": 1}
        with cycle_util.visit(d, path_ids) as visiting:
            self.assertTrue(visiting)
            with cycle_util.visit(d, path_ids) as visiting_again:
                self.assertFalse(visiting_again)
        # the value is removed from the path when leaving it
        self.assertEqual(path_ids, set())

    def test_visit_removes_value_from_path_on_error(self) -> None:
        path_ids: set[int] = set()
        with self.assertRaises(KeyError):
            with cycle_util.visit({}, path_ids):
                raise KeyError()
        self.assertEqual(path_ids, set())
