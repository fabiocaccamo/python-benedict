from __future__ import annotations

import unittest
from typing import Any

from benedict.core import clone as _clone
from benedict.core import traverse as _traverse


class traverse_test_case(unittest.TestCase):
    """
    This class describes a traverse test case.
    """

    def test_traverse(self) -> None:
        i = {
            "a": {
                "x": 2,
                "y": 3,
                "z": {
                    "ok": 5,
                },
            },
            "b": {
                "x": 7,
                "y": 11,
                "z": {
                    "ok": 13,
                },
            },
            "c": {
                "x": 17,
                "y": 19,
                "z": {
                    "ok": 23,
                },
            },
        }
        o = _clone(i)
        with self.assertRaises(ValueError):
            _traverse(o, True)  # type: ignore[arg-type]

        def f(parent: Any, key: Any, value: Any) -> None:
            if not isinstance(value, dict):
                parent[key] = value + 1

        _traverse(o, f)
        r = {
            "a": {
                "x": 3,
                "y": 4,
                "z": {
                    "ok": 6,
                },
            },
            "b": {
                "x": 8,
                "y": 12,
                "z": {
                    "ok": 14,
                },
            },
            "c": {
                "x": 18,
                "y": 20,
                "z": {
                    "ok": 24,
                },
            },
        }
        self.assertEqual(o, r)

    def test_traverse_self_referential_dict(self) -> None:
        i: dict[str, Any] = {"a": {"b": 1}}
        i["self"] = i
        keys: list[Any] = []
        _traverse(i, lambda d, key, value: keys.append(key))
        # the dict containing itself is visited once, without recursing forever
        self.assertEqual(keys, ["a", "b", "self"])

    def test_traverse_self_referential_list(self) -> None:
        ls: list[Any] = [{"a": 1}]
        ls.append(ls)
        i = {"x": ls}
        keys: list[Any] = []
        _traverse(i, lambda d, key, value: keys.append(key))
        self.assertEqual(keys, ["x", 0, "a", 1])

    def test_traverse_shared_references_are_visited_each_time(self) -> None:
        shared = {"x": 1}
        i = {"a": shared, "b": [shared, shared]}
        keys: list[Any] = []
        _traverse(i, lambda d, key, value: keys.append(key))
        # shared (non cyclic) references are not cycles and must still be visited
        self.assertEqual(keys, ["a", "x", "b", 0, "x", 1, "x"])
