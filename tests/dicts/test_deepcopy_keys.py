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
