import unittest

from benedict.core import keypaths as _keypaths


class keypaths_test_case(unittest.TestCase):
    """
    This class describes a keypaths test case.
    """

    def test_keypaths(self):
        i = {
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
            },
        }
        o = _keypaths(i)
        r = [
            "a",
            "b",
            "b.c",
            "b.c.x",
            "b.c.y",
            "b.d",
            "b.d.x",
            "b.d.y",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_custom_separator(self):
        i = {
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
            },
        }
        o = _keypaths(i, separator="/")
        r = [
            "a",
            "b",
            "b/c",
            "b/c/x",
            "b/c/y",
            "b/d",
            "b/d/x",
            "b/d/y",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_invalid_separator(self):
        i = {
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
            },
        }
        with self.assertRaises(ValueError):
            o = _keypaths(i, separator=True)

    def test_keypaths_without_separator(self):
        i = {
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
            },
        }
        # with self.assertRaises(ValueError):
        #     o = _keypaths(i, separator=None)
        o = _keypaths(i)
        r = [
            "a",
            "b",
            "b.c",
            "b.c.x",
            "b.c.y",
            "b.d",
            "b.d.x",
            "b.d.y",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_non_string_keys(self):
        i = {
            True: {
                True: 1,
            },
            False: {
                False: 1,
            },
            None: {
                None: 1,
            },
        }
        o = _keypaths(i)
        r = [
            "False",
            "False.False",
            "None",
            "None.None",
            "True",
            "True.True",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_lists_and_indexes_included(self):
        i = {
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
                "e": [
                    {
                        "x": 1,
                        "y": -1,
                        "z": [1, 2, 3],
                    },
                    {
                        "x": 2,
                        "y": -2,
                        "z": [2, 3, 4],
                    },
                    {
                        "x": 3,
                        "y": -3,
                        "z": [3, 4, 5],
                    },
                ],
            },
        }
        o = _keypaths(i, indexes=True)
        r = [
            "a",
            "b",
            "b.c",
            "b.c.x",
            "b.c.y",
            "b.d",
            "b.d.x",
            "b.d.y",
            "b.e",
            "b.e[0]",
            "b.e[0].x",
            "b.e[0].y",
            "b.e[0].z",
            "b.e[0].z[0]",
            "b.e[0].z[1]",
            "b.e[0].z[2]",
            "b.e[1]",
            "b.e[1].x",
            "b.e[1].y",
            "b.e[1].z",
            "b.e[1].z[0]",
            "b.e[1].z[1]",
            "b.e[1].z[2]",
            "b.e[2]",
            "b.e[2].x",
            "b.e[2].y",
            "b.e[2].z",
            "b.e[2].z[0]",
            "b.e[2].z[1]",
            "b.e[2].z[2]",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_lists_and_indexes_not_included(self):
        i = {
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
                "e": [
                    {
                        "x": 1,
                        "y": -1,
                        "z": [1, 2, 3],
                    },
                    {
                        "x": 2,
                        "y": -2,
                        "z": [2, 3, 4],
                    },
                    {
                        "x": 3,
                        "y": -3,
                        "z": [3, 4, 5],
                    },
                ],
            },
        }
        o = _keypaths(i, indexes=False)
        r = [
            "a",
            "b",
            "b.c",
            "b.c.x",
            "b.c.y",
            "b.d",
            "b.d.x",
            "b.d.y",
            "b.e",
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_nested_lists_and_indexes_included(self):
        i = {
            "a": {
                "b": [
                    [1, 2],
                    [3, 4, 5],
                    [
                        {
                            "x": 1,
                            "y": -1,
                        },
                    ],
                ],
            },
        }
        o = _keypaths(i, indexes=True)
        r = [
            "a",
            "a.b",
            "a.b[0]",
            "a.b[0][0]",
            "a.b[0][1]",
            "a.b[1]",
            "a.b[1][0]",
            "a.b[1][1]",
            "a.b[1][2]",
            "a.b[2]",
            "a.b[2][0]",
            "a.b[2][0].x",
            "a.b[2][0].y",
        ]
        self.assertEqual(o, r)
