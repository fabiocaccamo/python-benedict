import unittest

from benedict.core import remove as _remove


class remove_test_case(unittest.TestCase):
    """
    This class describes a remove test case.
    """

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
