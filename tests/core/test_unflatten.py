import unittest

from benedict.core import flatten as _flatten
from benedict.core import unflatten as _unflatten


class unflatten_test_case(unittest.TestCase):
    """
    This class describes an unflatten test case.
    """

    def test_unflatten(self) -> None:
        d = {
            "a": 1,
            "b_c": 2,
            "d_e": 3,
        }
        u = _unflatten(d)
        r = {
            "a": 1,
            "b": {
                "c": 2,
            },
            "d": {
                "e": 3,
            },
        }
        self.assertEqual(u, r)

    def test_unflatten_with_custom_separator(self) -> None:
        d = {
            "a": 1,
            "b|c": 2,
            "d|e": 3,
        }
        u = _unflatten(d, separator="#")
        self.assertEqual(u, d)
        u = _unflatten(d, separator="|")
        r = {
            "a": 1,
            "b": {
                "c": 2,
            },
            "d": {
                "e": 3,
            },
        }
        self.assertEqual(u, r)

    def test_unflatten_after_flatten_with_indexes_simple_list(self) -> None:
        i = {
            "a": 1,
            "b": ["x", "y", "z"],
        }
        f = _flatten(i, indexes=True)
        u = _unflatten(f)
        self.assertEqual(u, i)

    def test_unflatten_after_flatten_with_indexes_list_of_dicts(self) -> None:
        i = {
            "a": 1,
            "b": [
                {"c": 2},
                {"d": 3},
            ],
        }
        f = _flatten(i, indexes=True)
        u = _unflatten(f)
        self.assertEqual(u, i)

    def test_unflatten_after_flatten_with_indexes_nested_lists(self) -> None:
        i = {
            "a": [[1, 2], [3, 4]],
        }
        f = _flatten(i, indexes=True)
        u = _unflatten(f)
        self.assertEqual(u, i)

    def test_unflatten_after_flatten_with_indexes_complex(self) -> None:
        i = {
            "test": {
                "d10": {
                    "d11": "single",
                    "d12": {
                        "crontab": ["cron_01", "cron_02"],
                        "minidlna": ["mini_01", "mini_02"],
                    },
                    "d13": [
                        {"dict01": "ciao_01"},
                        {"dict02": "ciao_02"},
                    ],
                }
            }
        }
        f = _flatten(i, separator="/", indexes=True)
        u = _unflatten(f, separator="/")
        self.assertEqual(u, i)

    def test_unflatten_after_flatten_with_indexes_custom_separator(self) -> None:
        i = {
            "a": {
                "b": ["x", "y"],
                "c": 1,
            },
        }
        f = _flatten(i, separator="/", indexes=True)
        u = _unflatten(f, separator="/")
        self.assertEqual(u, i)

    def test_unflatten_after_flatten_with_indexes_empty_list(self) -> None:
        i = {
            "a": 1,
            "b": [],
        }
        f = _flatten(i, indexes=True)
        self.assertEqual(f, {"a": 1})
        u = _unflatten(f)
        self.assertEqual(u, {"a": 1})
        self.assertNotIn("b", u)

    def test_unflatten_with_nested_dict(self) -> None:
        d = {
            "a": 1,
            "b_c": {
                "u_v": 2,
            },
            "d_e": {
                "x_y_z": 3,
            },
        }
        u = _unflatten(d)
        r = {
            "a": 1,
            "b": {
                "c": {
                    "u": {
                        "v": 2,
                    },
                },
            },
            "d": {
                "e": {
                    "x": {
                        "y": {
                            "z": 3,
                        },
                    },
                },
            },
        }
        self.assertEqual(u, r)


class benedict_unflatten_test_case(unittest.TestCase):
    """
    This class describes unflattening benedict instances, where the
    keypath-aware get would otherwise lose list values (GH issue #655).
    """

    def test_benedict_unflatten_after_flatten_with_indexes(self) -> None:
        from benedict import benedict

        d = benedict({"top": [1, 2], "l": [{"a": 1}]})
        f = d.flatten(indexes=True)
        u = f.unflatten()
        self.assertEqual(u, {"top": [1, 2], "l": [{"a": 1}]})

    def test_benedict_unflatten_deep_nested(self) -> None:
        from benedict import benedict

        d = benedict({"a": {"b": [{"c": [1, 2, {"d": 3}]}]}})
        f = d.flatten(indexes=True)
        u = f.unflatten()
        self.assertEqual(u, {"a": {"b": [{"c": [1, 2, {"d": 3}]}]}})
        self.assertIsInstance(u, benedict)

    def test_plain_dict_unflatten_unchanged(self) -> None:
        d = {"top": [1, 2]}
        f = _flatten(d, indexes=True)
        u = _unflatten(f)
        self.assertEqual(u, {"top": [1, 2]})
