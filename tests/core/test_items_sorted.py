import unittest

from benedict.core import items_sorted_by_keys as _items_sorted_by_keys
from benedict.core import items_sorted_by_values as _items_sorted_by_values


class items_sorted_test_case(unittest.TestCase):
    """
    This class describes an items sorted test case.
    """

    def test_items_sorted_by_keys(self):
        i = {
            "y": 3,
            "a": 6,
            "f": 9,
            "z": 4,
            "x": 1,
        }
        o = _items_sorted_by_keys(i)
        r = [
            ("a", 6),
            ("f", 9),
            ("x", 1),
            ("y", 3),
            ("z", 4),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_keys_reverse(self):
        i = {
            "y": 3,
            "a": 6,
            "f": 9,
            "z": 4,
            "x": 1,
        }
        o = _items_sorted_by_keys(i, reverse=True)
        r = [
            ("z", 4),
            ("y", 3),
            ("x", 1),
            ("f", 9),
            ("a", 6),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_values(self):
        i = {
            "a": 3,
            "b": 6,
            "c": 9,
            "e": 4,
            "d": 1,
        }
        o = _items_sorted_by_values(i)
        r = [
            ("d", 1),
            ("a", 3),
            ("e", 4),
            ("b", 6),
            ("c", 9),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_values_reverse(self):
        i = {
            "a": 3,
            "b": 6,
            "c": 9,
            "e": 4,
            "d": 1,
        }
        o = _items_sorted_by_values(i, reverse=True)
        r = [
            ("c", 9),
            ("b", 6),
            ("e", 4),
            ("a", 3),
            ("d", 1),
        ]
        self.assertEqual(o, r)
