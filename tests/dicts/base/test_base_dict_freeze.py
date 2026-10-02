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

    def test_frozen_dict_supports_methods_that_return_a_new_dict(self) -> None:
        # These are documented as returning a new dict and do not mutate the
        # source, but each builds its result with clone(empty=True), which
        # used to clear a deep copy that had inherited the frozen flag.
        from benedict import benedict

        source = {"a": 1, "nested": {"x": 1, "y": 2}}

        b = benedict(source).freeze()
        self.assertEqual(
            dict(b.flatten()), {"a": 1, "nested_x": 1, "nested_y": 2}
        )

        b = benedict(source).freeze()
        self.assertEqual(dict(b.subset(["a"])), {"a": 1})

        b = benedict(source).freeze()
        self.assertEqual(dict(b.filter(lambda key, value: key == "a")), {"a": 1})

        b = benedict({"a_b": 1}).freeze()
        self.assertEqual(dict(b.unflatten()), {"a": {"b": 1}})

    def test_frozen_dict_is_unchanged_by_those_methods(self) -> None:
        from benedict import benedict

        b = benedict({"a": 1, "nested": {"x": 1}}).freeze()
        b.flatten()
        b.subset(["a"])
        self.assertTrue(b.frozen)
        self.assertEqual(dict(b), {"a": 1, "nested": {"x": 1}})
        with self.assertRaises(TypeError):
            b["z"] = 1

    def test_new_dict_from_a_frozen_dict_is_not_frozen(self) -> None:
        # The result is a fresh container the caller owns, so it is writable.
        from benedict import benedict

        result = benedict({"a": 1, "nested": {"x": 1}}).freeze().flatten()
        self.assertFalse(result.frozen)
        result["z"] = 1  # must not raise

    def test_clone_of_a_frozen_dict_stays_frozen(self) -> None:
        # Unchanged: a full clone keeps the frozen state, only the empty
        # clone used internally does not.
        from benedict import benedict

        clone = benedict({"a": 1}).freeze().clone()
        self.assertTrue(clone.frozen)

    def test_empty_clone_of_a_frozen_dict_keeps_its_settings(self) -> None:
        from benedict import benedict

        b = benedict({"a": {"b": 1}}, keypath_separator="/").freeze()
        self.assertEqual(b.flatten(separator="_")._keypath_separator, "/")
