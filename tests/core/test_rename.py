import unittest

from benedict.core import rename as _rename


class rename_test_case(unittest.TestCase):
    """
    This class describes a rename test case.
    """

    def test_rename(self) -> None:
        d = {
            "a": {
                "x": 1,
                "y": 1,
            },
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 3,
                "y": 3,
            },
        }
        _rename(d, "a", "d")
        r = {
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 3,
                "y": 3,
            },
            "d": {
                "x": 1,
                "y": 1,
            },
        }
        self.assertEqual(d, r)

    def test_rename_with_same_key(self) -> None:
        d = {
            "a": 1,
            "b": 2,
        }
        _rename(d, "a", "a")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(d, r)

    def test_rename_to_existing_name(self) -> None:
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        with self.assertRaises(KeyError):
            _rename(d, "a", "c")

    def test_rename_deep(self) -> None:
        d = {
            "fname": "Alice",
            "address": {
                "fname": "street",
                "city": "Rome",
            },
        }
        _rename(d, "fname", "first_name", deep=True)
        r = {
            "first_name": "Alice",
            "address": {
                "first_name": "street",
                "city": "Rome",
            },
        }
        self.assertEqual(d, r)

    def test_rename_deep_key_not_at_every_level(self) -> None:
        d = {
            "a": 1,
            "nested": {
                "b": 2,
                "c": 3,
            },
            "x": {
                "a": 10,
                "d": 4,
            },
        }
        _rename(d, "a", "z", deep=True)
        r = {
            "z": 1,
            "nested": {
                "b": 2,
                "c": 3,
            },
            "x": {
                "z": 10,
                "d": 4,
            },
        }
        self.assertEqual(d, r)

    def test_rename_deep_inside_list(self) -> None:
        d = {
            "users": [
                {"fname": "Alice", "age": 30},
                {"fname": "Bob", "age": 25},
            ],
        }
        _rename(d, "fname", "first_name", deep=True)
        r = {
            "users": [
                {"first_name": "Alice", "age": 30},
                {"first_name": "Bob", "age": 25},
            ],
        }
        self.assertEqual(d, r)

    def test_rename_deep_without_deep_leaves_nested_untouched(self) -> None:
        d = {
            "a": 1,
            "nested": {
                "a": 2,
            },
        }
        _rename(d, "a", "z")
        r = {
            "z": 1,
            "nested": {
                "a": 2,
            },
        }
        self.assertEqual(d, r)
