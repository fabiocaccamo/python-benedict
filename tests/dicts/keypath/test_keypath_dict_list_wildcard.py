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
        self.assertEqual(b["a.b[2].d[3][*]"], [0])

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
