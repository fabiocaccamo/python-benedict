import copy
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

    def test_freeze_prevents_delitem_keypath(self) -> None:
        for separator in (".", "/"):
            for key in (f"a{separator}b", ["a", "b"], "values[0]", ["values", 0]):
                with self.subTest(separator=separator, key=key):
                    b = benedict(
                        {"a": {"b": 1}, "values": [1, 2]},
                        keypath_separator=separator,
                    ).freeze()
                    with self.assertRaisesRegex(TypeError, "frozen"):
                        del b[key]
                    self.assertEqual(b, {"a": {"b": 1}, "values": [1, 2]})
                    self.assertTrue(b.frozen)

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

    def test_freeze_prevents_pop_keypath(self) -> None:
        for separator in (".", "/"):
            for key in (f"a{separator}b", ["a", "b"], "values[0]", ["values", 0]):
                for args in ((), (None,), ("fallback",)):
                    with self.subTest(separator=separator, key=key, args=args):
                        b = benedict(
                            {"a": {"b": 1}, "values": [1, 2]},
                            keypath_separator=separator,
                        ).freeze()
                        with self.assertRaisesRegex(TypeError, "frozen"):
                            b.pop(key, *args)
                        self.assertEqual(b, {"a": {"b": 1}, "values": [1, 2]})
                        self.assertTrue(b.frozen)

    def test_freeze_prevents_pop_missing_keypath_with_default(self) -> None:
        for key in ("missing", "a.missing", "missing.path", "values[5]"):
            for default in (None, "fallback"):
                with self.subTest(key=key, default=default):
                    b = benedict({"a": {"b": 1}, "values": [1, 2]}).freeze()
                    with self.assertRaisesRegex(TypeError, "frozen"):
                        b.pop(key, default)
                    self.assertEqual(b, {"a": {"b": 1}, "values": [1, 2]})

    def test_keypath_deletion_when_mutable(self) -> None:
        cases = (
            (".", "a.b", {"a": {"b": 1}}, {"a": {}}),
            ("/", "a/b", {"a": {"b": 1}}, {"a": {}}),
            (".", ["a", "b"], {"a": {"b": 1}}, {"a": {}}),
            (".", "values[0]", {"values": [1, 2]}, {"values": [2]}),
            (".", ["values", 0], {"values": [1, 2]}, {"values": [2]}),
        )
        for unfreeze in (False, True):
            for operation in ("del", "pop"):
                for separator, key, source, expected in cases:
                    with self.subTest(unfreeze=unfreeze, operation=operation, key=key):
                        b = benedict(copy.deepcopy(source), keypath_separator=separator)
                        if unfreeze:
                            b.freeze().unfreeze()
                        if operation == "del":
                            del b[key]
                        else:
                            self.assertEqual(b.pop(key, "fallback"), 1)
                        self.assertEqual(b, expected)
                        missing_key = f"missing{separator}path"
                        self.assertIsNone(b.pop(missing_key, None))
                        self.assertEqual(b.pop(missing_key, "fallback"), "fallback")
                        with self.assertRaises(KeyError):
                            b.pop(missing_key)

    def test_freeze_allows_direct_nested_mutation(self) -> None:
        b = benedict({"a": {"b": 1}, "values": [1, 2]}).freeze()
        child = b["a"]
        self.assertFalse(child.frozen)
        child["c"] = 2
        del child["b"]
        self.assertEqual(child.pop("c"), 2)
        self.assertEqual(b["values"].pop(0), 1)
        self.assertEqual(b, {"a": {}, "values": [2]})
        self.assertTrue(b.frozen)

    def test_freeze_prevents_merge(self) -> None:
        b = benedict({"a": {"b": 1}}).freeze()
        for other in ({"a": {"c": 2}}, {"d": 3}):
            with self.subTest(other=other):
                with self.assertRaisesRegex(TypeError, "frozen"):
                    b.merge(other)
                self.assertEqual(b, {"a": {"b": 1}})

    def test_freeze_prevents_keylist_deletion_on_base_classes(self) -> None:
        from benedict.dicts.keylist import KeylistDict
        from benedict.dicts.keypath import KeypathDict

        for cls in (KeylistDict, KeypathDict):
            for operation in ("del", "pop"):
                with self.subTest(cls=cls.__name__, operation=operation):
                    d = cls({"a": {"b": 1}})
                    d.freeze()
                    with self.assertRaisesRegex(TypeError, "frozen"):
                        if operation == "del":
                            del d[["a", "b"]]
                        else:
                            d.pop(["a", "b"])
                    self.assertEqual(d, {"a": {"b": 1}})

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
