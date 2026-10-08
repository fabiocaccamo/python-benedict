from __future__ import annotations

import unittest
from typing import Any

from benedict import benedict


class benedict_cyclic_test_case(unittest.TestCase):
    """
    This class describes a benedict self-referential (cyclic) structures test case.
    """

    def test_init_with_self_referential_list(self) -> None:
        ls: list[Any] = [{"a": 1}]
        ls.append(ls)
        b = benedict({"x": ls})
        self.assertEqual(b["x"][0], {"a": 1})
        self.assertIsInstance(b["x"][0], benedict)
        self.assertIs(b["x"][1], ls)

    def test_search_self_referential_dict(self) -> None:
        b = benedict({"a": {"b": 1}})
        b["self"] = b
        results = b.search("b", in_keys=True, in_values=False)
        self.assertEqual(results, [({"b": 1}, "b", 1)])

    def test_standardize_self_referential_dict(self) -> None:
        b = benedict({"First Name": "Alice"})
        b["self"] = b
        b.standardize()
        self.assertEqual(b["first_name"], "Alice")

    def test_traverse_self_referential_dict(self) -> None:
        b = benedict({"a": {"b": 1}})
        b["self"] = b
        keys: list[Any] = []
        b.traverse(lambda d, key, value: keys.append(key))
        self.assertEqual(keys, ["a", "b", "self"])
