import unittest
from collections.abc import Iterator

from benedict.core import remove as _remove


class remove_test_case(unittest.TestCase):
    """
    This class describes a remove test case.
    """

    def test_remove_legacy_sequence_keys(self) -> None:
        class Keys:
            def __getitem__(self, index: int) -> str:
                return ["a", "b"][index]

        data = {"a": 1, "b": 2, "keep": 3}
        _remove(data, Keys())
        self.assertEqual(data, {"keep": 3})

    def test_remove_preserves_iteration_errors(self) -> None:
        def keys() -> Iterator[str]:
            yield "a"
            raise TypeError("keys iteration failed")

        data = {"a": 1, "b": 2}
        with self.assertRaisesRegex(TypeError, "keys iteration failed"):
            _remove(data, keys())
        self.assertEqual(data, {"a": 1, "b": 2})

    def test_remove_scalar_nonstring_keys(self) -> None:
        for key in (0, 12, None):
            with self.subTest(key=key):
                data = {key: "removed", "keep": 1}
                _remove(data, key)
                self.assertEqual(data, {"keep": 1})

    def test_remove_scalar_keys_deep_and_with_args(self) -> None:
        data = {0: "top", 1: "other", "nested": {0: "child", "keep": 1}}
        _remove(data, 0, 1, deep=True)
        self.assertEqual(data, {"nested": {"keep": 1}})

    def test_remove_with_single_key(self) -> None:
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        _remove(d, "c")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_args(self) -> None:
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        _remove(d, "c", "d", "e")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_list(self) -> None:
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        _remove(d, ["c", "d", "e"])
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_remove_deep_with_single_key(self) -> None:
        d = {
            "a": 1,
            "b": {
                "password": "secret",
                "name": "test",
            },
            "password": "topsecret",
        }
        _remove(d, "password", deep=True)
        r = {
            "a": 1,
            "b": {
                "name": "test",
            },
        }
        self.assertEqual(d, r)

    def test_remove_deep_with_multiple_keys(self) -> None:
        d = {
            "a": 1,
            "secret": "x",
            "b": {
                "secret": "y",
                "token": "z",
                "name": "test",
                "c": {
                    "token": "w",
                    "value": 42,
                },
            },
        }
        _remove(d, ["secret", "token"], deep=True)
        r = {
            "a": 1,
            "b": {
                "name": "test",
                "c": {
                    "value": 42,
                },
            },
        }
        self.assertEqual(d, r)

    def test_remove_deep_inside_list(self) -> None:
        d = {
            "users": [
                {"name": "Alice", "password": "abc"},
                {"name": "Bob", "password": "xyz"},
            ],
            "password": "admin",
        }
        _remove(d, "password", deep=True)
        r = {
            "users": [
                {"name": "Alice"},
                {"name": "Bob"},
            ],
        }
        self.assertEqual(d, r)

    def test_remove_without_deep_leaves_nested_untouched(self) -> None:
        d = {
            "a": 1,
            "b": {
                "password": "secret",
            },
            "password": "topsecret",
        }
        _remove(d, "password")
        r = {
            "a": 1,
            "b": {
                "password": "secret",
            },
        }
        self.assertEqual(d, r)

    def test_remove_deep_inside_list_nested_in_dict(self) -> None:
        d = {
            "section": {
                "users": [
                    {"name": "Alice", "password": "abc"},
                    {"name": "Bob", "password": "xyz"},
                ],
            },
        }
        _remove(d, "password", deep=True)
        r = {
            "section": {
                "users": [
                    {"name": "Alice"},
                    {"name": "Bob"},
                ],
            },
        }
        self.assertEqual(d, r)

    def test_remove_deep_inside_tuple_nested_in_dict(self) -> None:
        d = {
            "section": {
                "users": (
                    {"name": "Alice", "password": "abc"},
                    {"name": "Bob", "password": "xyz"},
                ),
            },
        }
        _remove(d, "password", deep=True)
        r = {
            "section": {
                "users": (
                    {"name": "Alice"},
                    {"name": "Bob"},
                ),
            },
        }
        self.assertEqual(d, r)

    def test_remove_deep_inside_nested_lists(self) -> None:
        d = {"users": [[{"name": "Alice", "password": "abc", "token": "xyz"}]]}
        _remove(d, ["password"], "token", deep=True)
        self.assertEqual(d, {"users": [[{"name": "Alice"}]]})

    def test_remove_deep_inside_mixed_nested_sequences(self) -> None:
        d = {"users": ([({"name": "Alice", "password": "abc"},)],)}
        _remove(d, "password", deep=True)
        self.assertEqual(d, {"users": ([({"name": "Alice"},)],)})
