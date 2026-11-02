from __future__ import annotations

import copy
import unittest

from benedict import benedict
from benedict.dicts.base import BaseDict


class deepcopy_keys_test_case(unittest.TestCase):
    def test_base_deepcopy_custom_keys(self) -> None:
        class Key:
            def __init__(self) -> None:
                self.values: list[int] = []

        for wrapped in (False, True):
            for frozen in (False, True):
                with self.subTest(wrapped=wrapped, frozen=frozen):
                    key = Key()
                    source = {key: [key]}
                    original = BaseDict(source) if wrapped else BaseDict()
                    if not wrapped:
                        original[key] = source[key]
                    if frozen:
                        original.freeze()
                    cloned = copy.deepcopy(original)
                    cloned_key = next(iter(cloned))
                    self.assertIsNot(cloned_key, key)
                    self.assertIs(cloned[cloned_key][0], cloned_key)
                    self.assertEqual(cloned.frozen, frozen)
                    cloned_key.values.append(1)
                    self.assertEqual(key.values, [])
                    self.assertIs(next(iter(original)), key)

    def test_benedict_deepcopy_custom_keys(self) -> None:
        class Key:
            def __init__(self) -> None:
                self.values: list[int] = []

        for separator in (None, "/"):
            for frozen in (False, True):
                with self.subTest(separator=separator, frozen=frozen):
                    key = Key()
                    original = benedict(
                        {key: [key]},
                        keypath_separator=separator,
                        keyattr_enabled=False,
                        keyattr_dynamic=True,
                    )
                    if frozen:
                        original.freeze()
                    cloned = original.deepcopy()
                    cloned_key = next(iter(cloned))
                    self.assertIsNot(cloned_key, key)
                    self.assertIs(cloned[cloned_key][0], cloned_key)
                    self.assertEqual(cloned.frozen, frozen)
                    self.assertEqual(cloned.keypath_separator, separator)
                    self.assertFalse(cloned.keyattr_enabled)
                    self.assertTrue(cloned.keyattr_dynamic)
                    cloned_key.values.append(1)
                    self.assertEqual(key.values, [])


class deepcopy_backreference_test_case(unittest.TestCase):
    def test_key_backreference_uses_returned_clone(self) -> None:
        class Key:
            pass

        for cls in (BaseDict, benedict):
            for wrapped in (False, True):
                for frozen in (False, True):
                    with self.subTest(cls=cls, wrapped=wrapped, frozen=frozen):
                        key = Key()
                        original = cls({}) if wrapped else cls()
                        key.parent = original
                        original[key] = [key]
                        if frozen:
                            original.freeze()
                        memo = {}
                        cloned = copy.deepcopy(original, memo)
                        cloned_key = next(iter(cloned))
                        self.assertIs(cloned_key.parent, cloned)
                        self.assertIs(cloned[cloned_key][0], cloned_key)
                        self.assertIs(memo[id(original)], cloned)
                        self.assertEqual(cloned.frozen, frozen)
                        self.assertIs(key.parent, original)

    def test_value_object_backreference_uses_returned_clone(self) -> None:
        class Value:
            pass

        for cls in (BaseDict, benedict):
            with self.subTest(cls=cls):
                original = cls()
                value = Value()
                value.parent = original
                original["value"] = value
                cloned = copy.deepcopy(original)
                self.assertIs(cloned["value"].parent, cloned)
                self.assertIsNot(cloned["value"], value)

    def test_mutual_key_owner_references(self) -> None:
        class Key:
            pass

        for cls in (BaseDict, benedict):
            with self.subTest(cls=cls):
                first, second = cls(), cls()
                key1, key2 = Key(), Key()
                key1.owner, key1.other = first, second
                key2.owner, key2.other = second, first
                first[key1], second[key2] = 1, 2
                copied_first, copied_second = copy.deepcopy([first, second])
                copied_key1 = next(iter(copied_first))
                copied_key2 = next(iter(copied_second))
                self.assertIs(copied_key1.owner, copied_first)
                self.assertIs(copied_key1.other, copied_second)
                self.assertIs(copied_key2.owner, copied_second)
                self.assertIs(copied_key2.other, copied_first)

    def test_wrapped_mapping_memo_is_not_claimed_by_wrapper(self) -> None:
        for cls in (BaseDict, benedict):
            with self.subTest(cls=cls):
                backing = {"value": [1]}
                original = cls(backing)
                backing_clone = {"separate": True}
                memo = {id(backing): backing_clone}
                cloned = copy.deepcopy(original, memo)
                self.assertIs(memo[id(backing)], backing_clone)
                self.assertIs(memo[id(original)], cloned)
                self.assertIsNot(cloned, backing_clone)
                self.assertEqual(cloned, original)
                self.assertIsNot(cloned["value"], backing["value"])

    def test_mapping_self_cycles_still_rejected(self) -> None:
        for cls in (BaseDict, benedict):
            with self.subTest(cls=cls):
                source = cls()
                source["self"] = source
                with self.assertRaisesRegex(ValueError, "cyclic.*not supported"):
                    cls(source)
                self.assertEqual(cls._unwrapping_ids, set())

    def test_benedict_backreference_preserves_options(self) -> None:
        class Key:
            pass

        for separator in (None, "/"):
            for frozen in (False, True):
                with self.subTest(separator=separator, frozen=frozen):
                    original = benedict(
                        keypath_separator=separator,
                        keyattr_enabled=False,
                        keyattr_dynamic=True,
                    )
                    key = Key()
                    key.parent = original
                    original[key] = key
                    if frozen:
                        original.freeze()
                    cloned = original.deepcopy()
                    cloned_key = next(iter(cloned))
                    self.assertIs(cloned_key.parent, cloned)
                    self.assertIs(cloned[cloned_key], cloned_key)
                    self.assertEqual(cloned.keypath_separator, separator)
                    self.assertFalse(cloned.keyattr_enabled)
                    self.assertTrue(cloned.keyattr_dynamic)
                    self.assertEqual(cloned.frozen, frozen)
