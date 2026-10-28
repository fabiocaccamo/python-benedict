import unittest
from collections import namedtuple
from typing import Any

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

    def test_filter_deep_dicts_inside_sequences(self) -> None:
        source: dict[str, Any] = {
            "rows": [{"keep": 1, "drop": None}, ({"drop": None},)],
            "none": None,
        }
        result = _filter(source, lambda key, value: value is not None, deep=True)
        self.assertEqual(result, {"rows": [{"keep": 1}, ({},)]})
        self.assertEqual(source["rows"][0], {"keep": 1, "drop": None})
        self.assertIsInstance(result["rows"], list)
        self.assertIsInstance(result["rows"][1], tuple)

    def test_filter_deep_sequence_elements_are_not_predicate_items(self) -> None:
        seen: list[Any] = []
        source = {"rows": [None, 1, [{"drop": None, "keep": 2}]]}

        def predicate(key: Any, value: Any) -> bool:
            seen.append(key)
            return value is not None

        result = _filter(source, predicate, deep=True)
        self.assertEqual(result, {"rows": [None, 1, [{"keep": 2}]]})
        self.assertEqual(seen, ["rows", "drop", "keep"])

    def test_filter_deep_rejected_sequence_is_not_traversed(self) -> None:
        seen: list[Any] = []

        def predicate(key: Any, value: Any) -> bool:
            seen.append(key)
            return key != "rows"

        self.assertEqual(_filter({"rows": [{"child": 1}]}, predicate, deep=True), {})
        self.assertEqual(seen, ["rows"])

    def test_filter_deep_sequence_predicate_exception_leaves_source_unchanged(
        self,
    ) -> None:
        source = {"rows": [{"drop": None, "fail": 1}]}

        def predicate(key: Any, value: Any) -> bool:
            if key == "fail":
                raise ValueError("predicate failed")
            return value is not None

        with self.assertRaisesRegex(ValueError, "predicate failed"):
            _filter(source, predicate, deep=True)
        self.assertEqual(source, {"rows": [{"drop": None, "fail": 1}]})

    def test_filter_deep_preserves_sequence_subclasses(self) -> None:
        class Rows(list[Any]):
            pass

        row = namedtuple("Row", "values label")
        source = {"rows": Rows([row({"keep": 1, "drop": None}, "first")])}
        result = _filter(source, lambda key, value: value is not None, deep=True)
        self.assertIsInstance(result["rows"], Rows)
        self.assertIsInstance(result["rows"][0], row)
        self.assertEqual(result["rows"][0].values, {"keep": 1})
        self.assertEqual(result["rows"][0].label, "first")
        self.assertEqual(source["rows"][0].values, {"keep": 1, "drop": None})

    def test_filter_deep_preserves_scalar_sequence_elements(self) -> None:
        marker = object()
        result = _filter({"rows": [marker, None]}, lambda key, value: True, deep=True)
        self.assertIs(result["rows"][0], marker)
        self.assertIsNone(result["rows"][1])
