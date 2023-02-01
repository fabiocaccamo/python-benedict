import unittest

from benedict.dicts.keypath import KeypathDict


class keypath_dict_list_indexes_test_case(unittest.TestCase):
    """
    This class describes a KeypathDict list indexes test case.
    """

    def test_contains_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertTrue("a[0]" in b)
        self.assertTrue("a[1]" in b)
        self.assertTrue("a[2]" in b)
        self.assertTrue("a[-1]" in b)

    def test_contains_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertFalse("a[3]" in b)
        self.assertFalse("a[]" in b)

    def test_contains_with_nested_list(self):
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

        self.assertTrue("a.b[0].d[-1]" in b)
        self.assertTrue("a.b[1].d[-1]" in b)
        self.assertFalse("a.b[2].d[-1]" in b)

        self.assertTrue("a.b[0].d" in b)
        self.assertTrue("a.b[1].d" in b)
        self.assertFalse("a.b[2].d" in b)

        self.assertTrue("a.b[0]" in b)
        self.assertTrue("a.b[1]" in b)
        self.assertFalse("a.b[2]" in b)

    def test_delitem_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        del b["a[-1]"]
        del b["a[0]"]
        self.assertEqual(b, {"a": [2]})

    def test_delitem_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["a[5]"]

    def test_delitem_with_nested_list(self):
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

        del b["a.b[0].d[-1]"]
        self.assertEqual(b["a.b[0].d"], [1, 2, 3])

        del b["a.b[0].d"]
        self.assertEqual(b["a.b[0]"], {"c": 1})

        del b["a.b[0]"]
        self.assertEqual(
            b["a.b[0]"],
            {
                "c": 2,
                "d": [4, 5, 6, [0]],
            },
        )

    def test_getitem_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b["a[0]"], 1)
        self.assertEqual(b["a[1]"], 2)
        self.assertEqual(b["a[2]"], 3)

        self.assertEqual(b["a[-1]"], 3)
        self.assertEqual(b["a[-2]"], 2)
        self.assertEqual(b["a[-3]"], 1)

    def test_getitem_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            self.assertEqual(b["a[5]"], 1)

    def test_getitem_with_nested_list(self):
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

        self.assertEqual(b["a.b[0].c"], 1)
        self.assertEqual(b["a.b[0].d"], [1, 2, 3, [0]])
        self.assertEqual(b["a.b[0].d[0]"], 1)
        self.assertEqual(b["a.b[0].d[1]"], 2)
        self.assertEqual(b["a.b[0].d[2]"], 3)
        self.assertEqual(b["a.b[0].d[3][0]"], 0)

        self.assertEqual(b["a.b[1].c"], 2)
        self.assertEqual(b["a.b[1].d"], [4, 5, 6, [0]])
        self.assertEqual(b["a.b[1].d[0]"], 4)
        self.assertEqual(b["a.b[1].d[1]"], 5)
        self.assertEqual(b["a.b[1].d[2]"], 6)
        self.assertEqual(b["a.b[1].d[3][0]"], 0)

        self.assertEqual(b["a.b[2].c"], 3)
        self.assertEqual(b["a.b[2].d"], [7, 8, 9, [0]])
        self.assertEqual(b["a.b[2].d[0]"], 7)
        self.assertEqual(b["a.b[2].d[1]"], 8)
        self.assertEqual(b["a.b[2].d[2]"], 9)
        self.assertEqual(b["a.b[2].d[3][0]"], 0)

    def test_getitem_github_issue_feature_request(self):
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
        self.assertEqual(b['products[""0""].categories[1].name'], "OK 2")

    def test_get_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b.get("a[0]"), 1)
        self.assertEqual(b.get("a[1]"), 2)
        self.assertEqual(b.get("a[2]"), 3)

        self.assertEqual(b.get("a[-1]"), 3)
        self.assertEqual(b.get("a[-2]"), 2)
        self.assertEqual(b.get("a[-3]"), 1)

    def test_get_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a[3]", 1), 1)

    def test_get_with_nested_list(self):
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

        self.assertEqual(b.get("a.b[0].c"), 1)
        self.assertEqual(b.get("a.b[0].d"), [1, 2, 3, [0]])
        self.assertEqual(b.get("a.b[0].d[0]"), 1)
        self.assertEqual(b.get("a.b[0].d[1]"), 2)
        self.assertEqual(b.get("a.b[0].d[2]"), 3)
        self.assertEqual(b.get("a.b[0].d[3][0]"), 0)

        self.assertEqual(b.get("a.b[1].c"), 2)
        self.assertEqual(b.get("a.b[1].d"), [4, 5, 6, [0]])
        self.assertEqual(b.get("a.b[1].d[0]"), 4)
        self.assertEqual(b.get("a.b[1].d[1]"), 5)
        self.assertEqual(b.get("a.b[1].d[2]"), 6)
        self.assertEqual(b.get("a.b[1].d[3][0]"), 0)

        self.assertEqual(b.get("a.b[2].c"), 3)
        self.assertEqual(b.get("a.b[2].d"), [7, 8, 9, [0]])
        self.assertEqual(b.get("a.b[2].d[0]"), 7)
        self.assertEqual(b.get("a.b[2].d[1]"), 8)
        self.assertEqual(b.get("a.b[2].d[2]"), 9)
        self.assertEqual(b.get("a.b[2].d[3][0]"), 0)

    def test_list_indexes_with_quotes(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a['0']"), 1)
        self.assertEqual(b.get('a["0"]'), 1)
        self.assertEqual(b.get('a["0"]'), 1)
        self.assertEqual(b.get("a['0']"), 1)
        self.assertEqual(b.get("a['']"), None)
        self.assertEqual(b.get('a[""]'), None)
        self.assertEqual(b.get('a[""]'), None)
        self.assertEqual(b.get("a['']"), None)

    def test_pop_with_flat_list(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        self.assertEqual(b.pop("a[-1]"), 3)
        self.assertEqual(b.pop("a[0]"), 1)
        self.assertEqual(b.pop("a"), [2])

    def test_pop_with_flat_list_and_default(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)

        with self.assertRaises(KeyError):
            b.pop("a[3]")
        self.assertEqual(b.pop("a[3]", 4), 4)

    def test_pop_with_wrong_index(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            b.pop("a[5]")

    def test_pop_with_wrong_index_and_default(self):
        d = {
            "a": [1, 2, 3],
        }
        b = KeypathDict(d)
        self.assertEqual(b.pop("a[5]", 6), 6)

    def test_pop_with_nested_list(self):
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

        self.assertEqual(b.pop("a.b[0].d[-1]"), [0])
        self.assertEqual(b["a.b[0].d"], [1, 2, 3])

        self.assertEqual(b.pop("a.b[0].d"), [1, 2, 3])
        self.assertEqual(b["a.b[0]"], {"c": 1})

        self.assertEqual(b.pop("a.b[0]"), {"c": 1})
        self.assertEqual(
            b["a.b[0]"],
            {
                "c": 2,
                "d": [4, 5, 6, [0]],
            },
        )
