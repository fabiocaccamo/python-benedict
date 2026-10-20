import unittest
from collections.abc import ItemsView, ValuesView

from benedict import benedict


class github_issue_0636_test_case(unittest.TestCase):
    """
    This class describes a github issue 0636 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/636

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0636
    """

    def test_items_and_values_are_sized_views(self) -> None:
        # serializers such as toml-rs call len() on mapping.items()
        d = benedict({"foo": [{"bar": "baz"}], "nested": {"value": 1}})
        items = d.items()
        values = d.values()
        self.assertIsInstance(items, ItemsView)
        self.assertIsInstance(values, ValuesView)
        self.assertEqual(len(items), 2)
        self.assertEqual(len(values), 2)

    def test_nested_items_are_sized_views(self) -> None:
        d = benedict({"foo": [{"bar": "baz"}]})
        nested = d["foo"][0]
        self.assertIsInstance(nested, benedict)
        self.assertEqual(len(nested.items()), 1)
        self.assertEqual(list(nested.items()), [("bar", "baz")])

    def test_items_and_values_still_cast_nested_dicts(self) -> None:
        source = {"nested": {"value": 1}}
        d = benedict(source)
        ((key, value),) = d.items()
        self.assertEqual(key, "nested")
        self.assertIsInstance(value, benedict)
        self.assertIsInstance(list(d.values())[0], benedict)
        # casting keeps the pointer to the original dict
        value["value"] = 2
        self.assertEqual(source["nested"]["value"], 2)

    def test_items_and_values_reflect_mutations(self) -> None:
        d = benedict({"a": 1})
        items = d.items()
        values = d.values()
        d["b"] = {"c": 2}
        del d["a"]
        self.assertEqual(list(d.keys()), ["b"])
        self.assertEqual(list(items), [("b", {"c": 2})])
        self.assertEqual(list(values), [{"c": 2}])
        self.assertEqual(len(items), 1)

    def test_items_membership(self) -> None:
        d = benedict({"a": {"b": 1}})
        self.assertIn(("a", {"b": 1}), d.items())
        self.assertIn({"b": 1}, d.values())
        self.assertNotIn(("a", {"b": 2}), d.items())

    def test_items_membership_does_not_resolve_keypaths(self) -> None:
        # like dict.items(), membership only matches actual keys
        for d in (
            benedict({"a": {"b": 1}, "l": [1, 2], "x": 1}),
            benedict(a={"b": 1}, l=[1, 2], x=1),
        ):
            with self.subTest(pointer=d.dict() is not d):
                self.assertIn(("x", 1), d.items())
                self.assertNotIn(("a.b", 1), d.items())
                self.assertNotIn(("l[0]", 1), d.items())
                self.assertNotIn((["a", "b"], 1), d.items())
                self.assertNotIn(("missing", 1), d.items())
                self.assertNotIn("x", d.items())

    def test_items_and_values_are_reversible(self) -> None:
        for d in (
            benedict({"a": 1, "b": {"c": 2}}),
            benedict(a=1, b={"c": 2}),
        ):
            with self.subTest(pointer=d.dict() is not d):
                self.assertEqual(list(reversed(d.items())), [("b", {"c": 2}), ("a", 1)])
                self.assertEqual(list(reversed(d.values())), [{"c": 2}, 1])
                self.assertIsInstance(next(reversed(d.values())), benedict)
