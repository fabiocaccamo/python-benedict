from __future__ import annotations

import copy
import unittest

from benedict.dicts.base import BaseDict


class base_dict_freeze_test_case(unittest.TestCase):
    def test_freeze(self) -> None:
        b = BaseDict({"a": 1})
        self.assertFalse(b.frozen)
        b.freeze()
        self.assertTrue(b.frozen)

    def test_freeze_returns_self(self) -> None:
        b = BaseDict({"a": 1})
        self.assertIs(b.freeze(), b)

    def test_freeze_prevents_setitem(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b["a"] = 2
        with self.assertRaises(TypeError):
            b["b"] = 3

    def test_freeze_prevents_delitem(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            del b["a"]

    def test_freeze_prevents_clear(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.clear()

    def test_freeze_prevents_pop(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.pop("a")

    def test_freeze_prevents_setdefault(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.setdefault("b", 2)

    def test_freeze_prevents_update(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.update({"b": 2})

    def test_freeze_allows_read(self) -> None:
        b = BaseDict({"a": 1, "b": 2})
        b.freeze()
        self.assertEqual(b["a"], 1)
        self.assertIn("a", b)
        self.assertEqual(list(b.keys()), ["a", "b"])

    def test_unfreeze(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        self.assertTrue(b.frozen)
        b.unfreeze()
        self.assertFalse(b.frozen)

    def test_unfreeze_returns_self(self) -> None:
        b = BaseDict({"a": 1})
        self.assertIs(b.freeze().unfreeze(), b)

    def test_unfreeze_allows_setitem(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        b.unfreeze()
        b["a"] = 2
        self.assertEqual(b["a"], 2)

    def test_freeze_does_not_propagate_to_nested_dict(self) -> None:
        # freeze() only blocks top-level mutations (aligned with frozendict/MappingProxyType).
        # nested dicts are not frozen.
        b = BaseDict({"a": 1, "b": {"c": 2}})
        b.freeze()
        self.assertTrue(b.frozen)
        with self.assertRaises(TypeError):
            b["a"] = 99

    def test_freeze_does_not_propagate_to_dict_in_list(self) -> None:
        inner = BaseDict({"b": 1})
        b = BaseDict()
        super(BaseDict, b).__setitem__("a", [inner])  # type: ignore[call-arg]
        b.freeze()
        # top-level is frozen
        self.assertTrue(b.frozen)
        # nested BaseDict is NOT frozen (no deep propagation)
        self.assertFalse(inner.frozen)

    def test_unfreeze_allows_setitem_after_freeze(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        self.assertTrue(b.frozen)
        b.unfreeze()
        self.assertFalse(b.frozen)
        b["a"] = 2
        self.assertEqual(b["a"], 2)

    def test_copy_of_frozen_is_frozen(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        c = b.copy()
        self.assertTrue(c.frozen)
        with self.assertRaises(TypeError):
            c["a"] = 2

    def test_copy_of_unfrozen_is_not_frozen(self) -> None:
        b = BaseDict({"a": 1})
        c = b.copy()
        self.assertFalse(c.frozen)
        c["a"] = 2  # must not raise

    def test_deepcopy_of_frozen_is_frozen(self) -> None:
        b = BaseDict({"a": 1})
        b.freeze()
        c = copy.deepcopy(b)
        self.assertTrue(c.frozen)
        with self.assertRaises(TypeError):
            c["a"] = 2

    def test_deepcopy_of_unfrozen_is_not_frozen(self) -> None:
        b = BaseDict({"a": 1})
        c = copy.deepcopy(b)
        self.assertFalse(c.frozen)
        c["a"] = 2  # must not raise
