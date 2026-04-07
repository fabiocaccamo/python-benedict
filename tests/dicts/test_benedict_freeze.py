import unittest

from benedict import benedict


class benedict_freeze_test_case(unittest.TestCase):
    def test_freeze(self) -> None:
        b = benedict({"a": 1})
        self.assertFalse(b.frozen)
        b.freeze()
        self.assertTrue(b.frozen)

    def test_freeze_returns_self(self) -> None:
        b = benedict({"a": 1})
        self.assertIs(b.freeze(), b)

    def test_freeze_prevents_setitem(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b["a"] = 2
        with self.assertRaises(TypeError):
            b["b"] = 3

    def test_freeze_prevents_setitem_keypath(self) -> None:
        b = benedict({"a": {"b": 1}})
        b.freeze()
        with self.assertRaises(TypeError):
            b["a.b"] = 2

    def test_freeze_prevents_setattr(self) -> None:
        b = benedict({"a": 1}, keyattr_enabled=True)
        b.freeze()
        with self.assertRaises(TypeError):
            b.a = 2

    def test_freeze_prevents_delitem(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            del b["a"]

    def test_freeze_prevents_clear(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.clear()

    def test_freeze_prevents_pop(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.pop("a")

    def test_freeze_prevents_update(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        with self.assertRaises(TypeError):
            b.update({"b": 2})

    def test_freeze_allows_read(self) -> None:
        b = benedict({"a": {"b": 1}})
        b.freeze()
        self.assertEqual(b["a.b"], 1)
        self.assertIn("a", b)

    def test_unfreeze(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        self.assertTrue(b.frozen)
        b.unfreeze()
        self.assertFalse(b.frozen)

    def test_unfreeze_returns_self(self) -> None:
        b = benedict({"a": 1})
        self.assertIs(b.freeze().unfreeze(), b)

    def test_unfreeze_allows_setitem(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        b.unfreeze()
        b["a"] = 2
        self.assertEqual(b["a"], 2)

    def test_freeze_nested_dict_is_not_frozen(self) -> None:
        # freeze() only blocks top-level mutations (aligned with frozendict/MappingProxyType).
        # nested dicts are NOT frozen.
        b = benedict({"a": {"b": 1}})
        b.freeze()
        self.assertTrue(b.frozen)
        with self.assertRaises(TypeError):
            b["a"] = 99
        # nested is accessible but not frozen
        self.assertFalse(b["a"].frozen)

    def test_freeze_dict_in_list_is_not_frozen(self) -> None:
        # nested dicts inside lists are NOT frozen.
        b = benedict({"a": [{"b": 1}]})
        b.freeze()
        self.assertTrue(b.frozen)
        self.assertFalse(b["a"][0].frozen)

    def test_unfreeze_nested_dict(self) -> None:
        b = benedict({"a": {"b": 1}})
        b.freeze()
        b.unfreeze()
        self.assertFalse(b.frozen)
        b["a"] = {"b": 2}
        self.assertEqual(b["a"]["b"], 2)

    def test_clone_of_frozen_is_frozen(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        c = b.clone()
        self.assertTrue(c.frozen)
        with self.assertRaises(TypeError):
            c["a"] = 2

    def test_clone_of_unfrozen_is_not_frozen(self) -> None:
        b = benedict({"a": 1})
        c = b.clone()
        self.assertFalse(c.frozen)
        c["a"] = 2  # must not raise

    def test_copy_of_frozen_is_frozen(self) -> None:
        b = benedict({"a": 1})
        b.freeze()
        c = b.copy()
        self.assertTrue(c.frozen)
        with self.assertRaises(TypeError):
            c["a"] = 2

    def test_copy_of_unfrozen_is_not_frozen(self) -> None:
        b = benedict({"a": 1})
        c = b.copy()
        self.assertFalse(c.frozen)
        c["a"] = 2  # must not raise
