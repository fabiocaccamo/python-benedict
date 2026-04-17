import unittest

from benedict.core import flatten as _flatten


class flatten_test_case(unittest.TestCase):
    """
    This class describes a flatten test case.
    """

    def test_flatten(self) -> None:
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": {
                    "e": 3,
                    "f": 4,
                    "g": {
                        "h": 5,
                    },
                }
            },
        }
        o = _flatten(i)
        r = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_custom_separator(self) -> None:
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": {
                    "e": 3,
                    "f": 4,
                    "g": {
                        "h": 5,
                    },
                }
            },
        }
        o = _flatten(i, separator="/")
        r = {
            "a": 1,
            "b": 2,
            "c/d/e": 3,
            "c/d/f": 4,
            "c/d/g/h": 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_flat_list(self) -> None:
        i = {
            "a": 1,
            "b": ["x", "y", "z"],
        }
        o = _flatten(i, indexes=True)
        r = {
            "a": 1,
            "b[0]": "x",
            "b[1]": "y",
            "b[2]": "z",
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_list_of_dicts(self) -> None:
        i = {
            "a": 1,
            "b": [
                {"c": 2},
                {"d": 3},
            ],
        }
        o = _flatten(i, indexes=True)
        r = {
            "a": 1,
            "b[0]_c": 2,
            "b[1]_d": 3,
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_nested_lists(self) -> None:
        i = {
            "a": [[1, 2], [3, 4]],
        }
        o = _flatten(i, indexes=True)
        r = {
            "a[0][0]": 1,
            "a[0][1]": 2,
            "a[1][0]": 3,
            "a[1][1]": 4,
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_complex(self) -> None:
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
        o = _flatten(i, separator="/", indexes=True)
        r = {
            "test/d10/d11": "single",
            "test/d10/d12/crontab[0]": "cron_01",
            "test/d10/d12/crontab[1]": "cron_02",
            "test/d10/d12/minidlna[0]": "mini_01",
            "test/d10/d12/minidlna[1]": "mini_02",
            "test/d10/d13[0]/dict01": "ciao_01",
            "test/d10/d13[1]/dict02": "ciao_02",
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_false_keeps_lists(self) -> None:
        i = {
            "a": 1,
            "b": ["x", "y", "z"],
        }
        o = _flatten(i, indexes=False)
        r = {
            "a": 1,
            "b": ["x", "y", "z"],
        }
        self.assertEqual(o, r)

    def test_flatten_with_indexes_tuple(self) -> None:
        i = {
            "a": (1, 2, 3),
        }
        o = _flatten(i, indexes=True)
        r = {
            "a[0]": 1,
            "a[1]": 2,
            "a[2]": 3,
        }
        self.assertEqual(o, r)

    def test_flatten_with_key_conflict(self) -> None:
        i = {
            "a": 1,
            "b": 2,
            "c": {
                "d": 3,
            },
            "c_d": 4,
            "d_e": 5,
            "d": {
                "e": 6,
            },
        }
        with self.assertRaises(KeyError):
            _ = _flatten(i)
        # r = {
        #     'a': 1,
        #     'b': 2,
        #     'c_d': 4,
        #     'd_e': 5,
        # }
        # self.assertEqual(o, r)
