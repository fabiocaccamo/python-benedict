import unittest

from benedict.core import merge as _merge


class merge_test_case(unittest.TestCase):
    """
    This class describes a merge test case.
    """

    def test_merge_with_flatten_dict(self):
        d = {
            "a": 1,
            "b": 1,
        }
        m = {
            "b": 2,
            "c": 3,
        }
        _merge(d, m)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        self.assertEqual(d, r)

    def test_merge_with_lists(self):
        d = {
            "a": [0, 1, 2],
            "b": [5, 6, 7],
            "c": [],
            "d": [],
        }
        m = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
        }
        _merge(d, m)
        r = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
            "d": [],
        }
        self.assertEqual(d, r)

    def test_merge_with_lists_and_concat(self):
        d = {
            "a": [0, 1, 2],
            "b": [5, 6, 7],
            "c": [],
            "d": [],
        }
        m = {
            "a": [3, 4, 5],
            "b": [8, 9, 0],
            "c": [-1],
        }
        _merge(d, m, concat=True)
        r = {
            "a": [0, 1, 2, 3, 4, 5],
            "b": [5, 6, 7, 8, 9, 0],
            "c": [-1],
            "d": [],
        }
        self.assertEqual(d, r)

    def test_merge_with_multiple_dicts(self):
        d = {
            "a": 1,
            "b": 1,
        }
        a = {
            "b": 2,
            "c": 3,
            "d": 3,
        }
        b = {
            "d": 5,
            "e": 5,
        }
        c = {
            "d": 4,
            "f": 6,
        }
        _merge(d, a, b, c)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        self.assertEqual(d, r)

    def test_merge_with_nested_dict(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                },
                "e": {
                    "x": 6,
                    "y": 7,
                },
            },
        }
        m = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                },
            },
        }
        _merge(d, m)
        r = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "x": 4,
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                    "x": 6,
                    "y": 7,
                },
            },
        }
        self.assertEqual(d, r)

    def test_merge_without_overwrite(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                },
                "e": {
                    "x": 6,
                    "y": 7,
                },
            },
        }
        m = {
            "a": 0,
            "b": {
                "c": 1,
                "d": {
                    "y": 1,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                },
            },
        }
        _merge(d, m, overwrite=False)
        r = {
            "a": 1,
            "b": {
                "c": {
                    "x": 2,
                    "y": 3,
                },
                "d": {
                    "x": 4,
                    "y": 5,
                    "z": 2,
                },
                "e": {
                    "f": {
                        "x": 2,
                        "y": 3,
                    },
                    "g": {
                        "x": 4,
                        "y": 5,
                    },
                    "x": 6,
                    "y": 7,
                },
            },
        }
        self.assertEqual(d, r)
