import unittest

from benedict.core import filter as _filter


class filter_test_case(unittest.TestCase):
    """
    This class describes a filter test case.
    """

    def test_filter(self) -> None:
        i = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        with self.assertRaises(ValueError):
            _filter(i, True)  # type: ignore[arg-type]
        o = _filter(i, lambda key, val: isinstance(val, int))
        r = {
            "a": 1,
            "b": 2,
            "f": 6,
            "g": 7,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_filter_deep(self) -> None:
        i = {
            "a": 1,
            "b": "hello",
            "nested": {
                "c": 2,
                "d": "world",
            },
        }
        o = _filter(i, lambda key, val: not isinstance(val, str), deep=True)
        r = {
            "a": 1,
            "nested": {
                "c": 2,
            },
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_filter_deep_predicate_removes_nested_dict_entirely(self) -> None:
        i = {
            "a": 1,
            "metadata": {
                "tag": "draft",
                "reviewed": "no",
            },
        }
        # predicate keeps only int values; the nested dict itself passes
        # (it is not a str), so it is kept but its children are filtered
        o = _filter(i, lambda key, val: not isinstance(val, str), deep=True)
        r = {
            "a": 1,
            "metadata": {},
        }
        self.assertEqual(o, r)

    def test_filter_deep_nested_dict_removed_by_predicate(self) -> None:
        i = {
            "a": 1,
            "private": {
                "secret": "x",
            },
        }
        # predicate rejects key "private" at top level → nested dict excluded entirely
        o = _filter(i, lambda key, val: key != "private", deep=True)
        r = {
            "a": 1,
        }
        self.assertEqual(o, r)

    def test_filter_deep_without_deep_leaves_nested_untouched(self) -> None:
        i = {
            "a": 1,
            "b": "hello",
            "nested": {
                "c": 2,
                "d": "world",
            },
        }
        o = _filter(i, lambda key, val: not isinstance(val, str))
        # nested dict passes predicate (it is not a str), so it is kept as-is
        r = {
            "a": 1,
            "nested": {
                "c": 2,
                "d": "world",
            },
        }
        self.assertEqual(o, r)
