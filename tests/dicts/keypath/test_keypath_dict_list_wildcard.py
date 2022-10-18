import unittest

from benedict.dicts import KeypathDict


class keypath_dict_list_wildcard_test_case(unittest.TestCase):
    def test_correct_wildcard(self):
        self.kd = KeypathDict(
            {
                "a": [
                    {"x": 1, "y": 1},
                    {"x": 2, "y": 2},
                ],
            }
        )
        correct_wildcard_path_example = "a[*].x"
        self.assertEqual(self.kd[correct_wildcard_path_example], [1, 2])

    def test_wildcard_contains_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertTrue("a[*]" in b)

    def test_wildcard_contains_with_wrong_property(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertFalse("b[*]" in b)

    def test_wildcard_contains_with_nested_list(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "d": [4, 5, 6, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)

        self.assertTrue("a.b[0].d[*]" in b)
        self.assertTrue("a.b[1].d[*]" in b)
        self.assertTrue("a.b[*]" in b)
        self.assertFalse("a.c[*]" in b)
        self.assertFalse("a.b.c[*]" in b)
        self.assertFalse("a.b.c[0]" in b)
        self.assertFalse("a.b.c[1]" in b)
        self.assertFalse("a.b.c[2]" in b)
        self.assertFalse("a.b[0].c[*]" in b)
        self.assertTrue("a.b[0].d[*][*]" in b)
        self.assertTrue("a.b[1].d[*][*]" in b)

    def test_wildcard_delitem_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        del b["a[*]"]
        self.assertEqual(b, {"a": []})
        d1 = {
            "a": [1, 2, 3],
        }
        b1 = KeypathDict(d1)
        del b1["a[-1]"]
        del b1["a[1]"]
        del b1["a[0]"]
        self.assertEqual(b, {"a": []})
        self.assertEqual(True, b == b1)

    def test_wildcard_delitem_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["b[*]"]

    def test_wildcard_delitem_with_nested_list(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "d": [4, 5, 6, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)

        del b["a.b[0].d[*]"]
        self.assertEqual(b["a.b[0].d"], [])

        del b["a.b[0].d"]
        self.assertEqual(b["a.b[0]"], {"c": 1})

        del b["a.b[*]"]
        self.assertEqual(b["a.b"], [])

    def test_wildcard_getitem_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b["a[*]"], [1, 2, 3])

    def test_wildcard_getitem_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            self.assertEqual(b["b[*]"], 1)

    def test_wildcard_getitem_with_nested_list(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "d": [4, 5, 6, [0]],
                    },
                    {
                        "c": 3,
                        "d": [7, 8, 9, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)

        self.assertEqual(b["a.b[0].d[*]"], [1, 2, 3, [0]])
        self.assertEqual(b["a.b[1].d[*]"], [4, 5, 6, [0]])
        self.assertEqual(b["a.b[2].d[*]"], [7, 8, 9, [0]])

        self.assertEqual(
            b["a.b[*]"],
            [
                {
                    "c": 1,
                    "d": [1, 2, 3, [0]],
                },
                {
                    "c": 2,
                    "d": [4, 5, 6, [0]],
                },
                {
                    "c": 3,
                    "d": [7, 8, 9, [0]],
                },
            ],
        )
        self.assertEqual(b["a.b[2].d[3][0]"], 0)
        self.assertEqual(b["a.b[2].d[3][*]"], [0])
        with self.assertRaises(KeyError):
            self.assertEqual(b["a.b[2].d[3][2]"], 0)

    def test_wildcard_getitem_github_issue_feature_request(self):
        d = {
            "products": [
                {
                    "categories": [
                        {
                            "name": "OK 1",
                        },
                        {
                            "name": "OK 2",
                        },
                    ],
                },
            ],
        }
        b = KeypathDict(d)
        self.assertEqual(
            b['products[""0""].categories[*]'],
            [
                {
                    "name": "OK 1",
                },
                {
                    "name": "OK 2",
                },
            ],
        )

    def test_wildcard_get_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b.get("a[*]"), [1, 2, 3])

    def test_wildcard_get_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("b[*]", 1), 1)

    def test_wildcard_get_with_nested_list(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "d": [4, 5, 6, [0]],
                    },
                    {
                        "c": 3,
                        "d": [7, 8, 9, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)

        self.assertEqual(b.get("a.b[0].d[*]"), [1, 2, 3, [0]])
        self.assertEqual(b.get("a.b[1].d[*]"), [4, 5, 6, [0]])
        self.assertEqual(b.get("a.b[2].d[*]"), [7, 8, 9, [0]])

        self.assertEqual(
            b["a.b[*]"],
            [
                {
                    "c": 1,
                    "d": [1, 2, 3, [0]],
                },
                {
                    "c": 2,
                    "d": [4, 5, 6, [0]],
                },
                {
                    "c": 3,
                    "d": [7, 8, 9, [0]],
                },
            ],
        )
        self.assertEqual(b.get("a.b[2].d[3][*]"), [0])

    def test_wildcard_list_indexes_with_quotes(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a['*']"), [1, 2, 3])
        self.assertEqual(b.get('a["*"]'), [1, 2, 3])

    def test_wildcard_pop_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b.pop("a[*]"), [1, 2, 3])
        self.assertEqual(b, {})

    def test_wildcard_pop_with_flat_list_and_default(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        with self.assertRaises(KeyError):
            b.pop("b[*]")
        self.assertEqual(b.pop("b[*]", 4), 4)

    def test_wildcard_pop_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            b.pop("b[*]")

    def test_wildcard_pop_with_wrong_index_and_default(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.pop("b[*]", 6), 6)

    def test_wildcard_pop_with_nested_list(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "d": [4, 5, 6, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)

        self.assertEqual(b.pop("a.b[0].d[-1][*]"), [0])
        self.assertEqual(b["a.b[0].d"], [1, 2, 3])

        self.assertEqual(b.pop("a.b[0].d[*]"), [1, 2, 3])
        self.assertEqual(b["a.b[0]"], {"c": 1})

        self.assertEqual(b.pop("a.b[0]"), {"c": 1})
        self.assertEqual(
            b["a.b[0]"],
            {
                "c": 2,
                "d": [4, 5, 6, [0]],
            },
        )

    def test_wildcard_asterix_as_key(self):
        d = {
            "*": {
                "b": [
                    {
                        "*": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "*": [4, 5, 6, [0]],
                    },
                ],
            },
        }
        b = KeypathDict(d)
        self.assertTrue(
            b["*"],
            {
                "b": [
                    {
                        "*": 1,
                        "d": [1, 2, 3, [0]],
                    },
                    {
                        "c": 2,
                        "*": [4, 5, 6, [0]],
                    },
                ],
            },
        )
        self.assertTrue(b["*.b[0].*"], 1)
        self.assertTrue(b.get("*.b[0].*", 2), 1)

        # wrong index => default value should be used
        self.assertTrue(b.get("*.b[2].*", 2), 2)
        self.assertTrue(b["*.b[1][*]"], [4, 5, 6, [0]])

        with self.assertRaises(KeyError):
            self.assertFalse(b["*.a"], None)
        with self.assertRaises(KeyError):
            self.assertFalse(b["*.*"], None)

        self.assertEqual(b.get("*.*", "not-existing"), "not-existing")

    def test_complex_wildcard_usage(self):
        d = {
            "a": {
                "b": [
                    {
                        "c": [
                            {"x": 10, "y": 20},
                            {"x": 11, "y": 21},
                            {"x": 12, "y": 22},
                        ],
                    },
                    {
                        "c": [
                            {"x": 20, "y": 30},
                            {"x": 21, "y": 31},
                            {"x": 22, "y": 32},
                        ],
                    },
                ],
            },
        }
        b = KeypathDict(d)
        self.assertEqual(
            b.get("a.b[0]"),
            {
                "c": [
                    {"x": 10, "y": 20},
                    {"x": 11, "y": 21},
                    {"x": 12, "y": 22},
                ],
            },
        )
        self.assertEqual(
            b.get("a.b[*]"),
            [
                {
                    "c": [
                        {"x": 10, "y": 20},
                        {"x": 11, "y": 21},
                        {"x": 12, "y": 22},
                    ],
                },
                {
                    "c": [
                        {"x": 20, "y": 30},
                        {"x": 21, "y": 31},
                        {"x": 22, "y": 32},
                    ],
                },
            ],
        )
        self.assertEqual(
            b.get("a.b[0].c"),
            [
                {"x": 10, "y": 20},
                {"x": 11, "y": 21},
                {"x": 12, "y": 22},
            ],
        )
        self.assertEqual(
            b.get("a.b[1].c"),
            [
                {"x": 20, "y": 30},
                {"x": 21, "y": 31},
                {"x": 22, "y": 32},
            ],
        )
        self.assertEqual(b.get("a.b[1].c[1]"), {"x": 21, "y": 31})
        self.assertEqual(
            b.get("a.b[*].c"),
            [
                [{"x": 10, "y": 20}, {"x": 11, "y": 21}, {"x": 12, "y": 22}],
                [{"x": 20, "y": 30}, {"x": 21, "y": 31}, {"x": 22, "y": 32}],
            ],
        )
        self.assertEqual(
            b.get("a.b[*].c[*].x"),
            [10, 11, 12, 20, 21, 22],
        )
        self.assertEqual(
            b.get("a.b[*].c[*].x[-1]"),
            22,
        )

    def test_complex_wildcard_non_consecutive(self):
        d = {
            "a": [
                {
                    "b": [
                        {
                            "c": {
                                "d": [
                                    {"x": 10, "y": 20},
                                    {"x": 11, "y": 21},
                                    {"x": 12, "y": 22},
                                ],
                                "e": [
                                    {"x": 20, "y": 30},
                                    {"x": 21, "y": 31},
                                    {"x": 22, "y": 32},
                                ],
                            },
                            "l": {"m": 2},
                        },
                    ],
                }
            ],
        }
        b = KeypathDict(d)
        self.assertEqual(
            b["a[*].b[*].c.d"],
            [
                {"x": 10, "y": 20},
                {"x": 11, "y": 21},
                {"x": 12, "y": 22},
            ],
        )
        self.assertEqual(
            b["a[*].b[*].c.d[*].x"],
            [10, 11, 12],
        )
