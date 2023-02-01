import unittest

from benedict.dicts.keypath import KeypathDict


class keypath_dict_test_case(unittest.TestCase):
    """
    This class describes a KeypathDict test case.
    """

    def test_init_with_custom_separator(self):
        d = {
            "a.b": {
                "c.d": 1,
                "e.f": 2,
            },
            "g.h": {
                "i.j": 3,
                "k.l": 4,
            },
        }
        b = KeypathDict(d, keypath_separator="/")
        self.assertEqual(b.get("a.b/c.d"), 1)
        self.assertEqual(b.get("a.b/e.f"), 2)
        self.assertEqual(b.get("g.h/i.j"), 3)
        self.assertEqual(b.get("g.h/k.l"), 4)

    def test_init_without_keypath_separator(self):
        d = {
            "a": {
                "b": 1,
                "c": 2,
            },
            "d": {
                "e": 3,
                "f": 4,
            },
        }
        b = KeypathDict(d, keypath_separator=None)
        self.assertEqual(b.get("a.b"), None)
        self.assertEqual(b.get("a.c"), None)
        self.assertEqual(b.get("d.e"), None)
        self.assertEqual(b.get("d.f"), None)

    def test_init_with_dict_with_separator_in_keys(self):
        d = {
            "a.b.c": 1,
            "c.d.e": 2,
        }
        with self.assertRaises(ValueError):
            KeypathDict(d)

    def test_update_with_dict_with_separator_in_keys(self):
        d1 = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        d2 = {
            "a.x": 4,
            "a.y": 5,
            "a.z": 6,
        }
        b = KeypathDict(d1)
        with self.assertRaises(ValueError):
            b.update(d2)

    def test_update_with_dict_without_separator_in_keys(self):
        d1 = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        d2 = {
            "a.x": 4,
            "a.y": 5,
            "a.z": 6,
        }
        b = KeypathDict(d1, keypath_separator="/")
        b.update(d2)
        self.assertEqual(b.get("a"), 1)
        self.assertEqual(b.get("b"), 2)
        self.assertEqual(b.get("c"), 3)
        self.assertEqual(b.get("a.x"), 4)
        self.assertEqual(b.get("a.y"), 5)
        self.assertEqual(b.get("a.z"), 6)

    def test_fromkeys(self):
        k = [
            "a",
            "a.b",
            "a.b.c",
            "a.b.d",
            "a.b.e",
            "x",
            "x.y",
            "x.z",
        ]
        b = KeypathDict.fromkeys(k)
        r = {
            "x": {
                "y": None,
                "z": None,
            },
            "a": {
                "b": {
                    "c": None,
                    "d": None,
                    "e": None,
                },
            },
        }
        self.assertEqual(b, r)

    def test_fromkeys_with_value(self):
        k = [
            "a",
            "a.b",
            "a.b.c",
            "a.b.d",
            "a.b.e",
            "x",
            "x.y",
            "x.z",
        ]
        b = KeypathDict.fromkeys(k, True)
        r = {
            "x": {
                "y": True,
                "z": True,
            },
            "a": {
                "b": {
                    "c": True,
                    "d": True,
                    "e": True,
                },
            },
        }
        self.assertEqual(b, r)

    def test_get_with_1_valid_key(self):
        d = {
            "a": 1,
            1: 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a", 2), 1)
        self.assertEqual(b.get(1, 2), 1)

    def test_get_with_1_invalid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("b", 2), 2)

    def test_get_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get(None, 1), None)
        self.assertEqual(b.get(False, True), False)
        self.assertEqual(b.get(True, True), True)
        self.assertEqual(b.get(0, 1), 0)

    def test_getitem_with_1_valid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b["a"], 1)

    def test_getitem_with_1_invalid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b["b"]
            # print(val)

    def test_getitem_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
            # 0: 0,
        }
        b = KeypathDict(d)
        self.assertEqual(b[None], None)
        self.assertEqual(b[False], False)
        with self.assertRaises(KeyError):
            val = b[True]
            # print(val)

        self.assertEqual(b[0], 0)

    def test_get_with_2_valid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a.b", 2), 1)

    def test_get_with_2_invalid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("b.a", 2), 2)

    def test_getitem_with_2_valid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b["a.b"], 1)

    def test_getitem_with_2_invalid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b["b.a"]
            # print(val)

    def test_get_with_3_valid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("a.b.c", 2), 1)

    def test_get_with_3_invalid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get("c.b.a", 2), 2)

    def test_get_with_empty_keys_list(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get([]), None)

    def test_get_with_keys_list(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d)
        self.assertEqual(b.get([]), None)
        self.assertEqual(
            b.get(["a"]),
            {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        )
        self.assertEqual(b.get(["a", "b.c"]), 1)
        self.assertEqual(b.get(["a", "b", "c"]), 1)
        self.assertEqual(b.get(["a", "b", "d"]), 2)
        self.assertEqual(b.get(["a", "b", "e"]), None)

    def test_get_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d, keypath_separator=None)
        self.assertEqual(b.get(["a", "b.c"]), None)
        self.assertEqual(b.get(["a", "b", "c"]), 1)
        self.assertEqual(b.get(["a", "b", "d"]), 2)
        self.assertEqual(b.get(["a", "b", "e"]), None)

    def test_getitem_with_3_valid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b["a.b.c"], 1)

    def test_getitem_with_3_invalid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b["c.b.a"]
            # print(val)

    def test_get_item_with_keys_list(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d)
        self.assertEqual(b["a", "b.c"], 1)
        self.assertEqual(b[["a", "b.c"]], 1)
        self.assertEqual(b[("a", "b.c")], 1)
        self.assertEqual(b["a", "b", "c"], 1)
        self.assertEqual(b[["a", "b", "c"]], 1)
        self.assertEqual(b[("a", "b", "c")], 1)
        self.assertEqual(b["a", "b", "d"], 2)
        self.assertEqual(b[["a", "b", "d"]], 2)
        self.assertEqual(b[("a", "b", "d")], 2)
        with self.assertRaises(KeyError):
            val = b["a", "b", "e"]
            # print(val)

    def test_get_item_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d, keypath_separator=None)
        with self.assertRaises(KeyError):
            val = b["a", "b.c"]
            # print(val)
        self.assertEqual(b["a", "b", "c"], 1)
        self.assertEqual(b[["a", "b", "c"]], 1)
        self.assertEqual(b[("a", "b", "c")], 1)
        self.assertEqual(b["a", "b", "d"], 2)
        self.assertEqual(b[["a", "b", "d"]], 2)
        self.assertEqual(b[("a", "b", "d")], 2)
        with self.assertRaises(KeyError):
            val = b["a", "b", "e"]
            # print(val)

    def test_has_with_1_key(self):
        d = {
            "a": 0,
            "b": None,
            "c": {},
        }
        b = KeypathDict(d)
        self.assertTrue("a" in b)
        self.assertTrue("b" in b)
        self.assertTrue("c" in b)
        self.assertFalse("d" in b)

    def test_has_with_2_keys(self):
        d = {
            "a": {
                "a": 0,
                "b": None,
                "c": {},
            },
        }
        b = KeypathDict(d)
        self.assertTrue("a.a" in b)
        self.assertTrue("a.b" in b)
        self.assertTrue("a.c" in b)
        self.assertFalse("a.d" in b)
        self.assertFalse("b" in b)
        self.assertFalse("b.a" in b)

    def test_has_with_3_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 0,
                    "d": None,
                    "e": {},
                    "x": [1, 2, 3],
                },
            },
        }
        b = KeypathDict(d)
        self.assertTrue("a.b.c" in b)
        self.assertTrue("a.b.d" in b)
        self.assertTrue("a.b.e" in b)
        self.assertFalse("a.b.f" in b)
        self.assertFalse("b.f" in b)
        self.assertFalse("f" in b)

        self.assertTrue("a.b.x[-1]" in b)
        self.assertTrue("a.b.x[0]" in b)
        self.assertTrue("a.b.x[1]" in b)
        self.assertTrue("a.b.x[2]" in b)
        self.assertFalse("a.b.x[3]" in b)

        self.assertFalse(0 in b["a.b.x"])
        self.assertTrue(1 in b["a.b.x"])
        self.assertTrue(2 in b["a.b.x"])
        self.assertTrue(3 in b["a.b.x"])
        self.assertFalse(4 in b["a.b.x"])

    def test_has_with_keys_list(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                    "x": [1, 2, 3],
                },
            },
        }
        b = KeypathDict(d)
        self.assertTrue(["a", "b.c"] in b)
        self.assertTrue(["a", "b", "c"] in b)
        self.assertTrue(["a", "b", "d"] in b)
        self.assertFalse(["a", "b", "e"] in b)
        self.assertTrue(["a", "b", "x", -1] in b)
        self.assertTrue(["a", "b", "x", 0] in b)
        self.assertTrue(["a", "b", "x", 1] in b)
        self.assertTrue(["a", "b", "x", 2] in b)
        self.assertFalse(["a", "b", "x", 3] in b)

    def test_has_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d, keypath_separator=None)
        self.assertFalse(["a", "b.c"] in b)
        self.assertTrue(["a", "b", "c"] in b)
        self.assertTrue(["a", "b", "d"] in b)
        self.assertFalse(["a", "b", "e"] in b)

    def test_keypath_separator_getter_setter(self):
        d = KeypathDict({}, keypath_separator=None)
        self.assertEqual(d.keypath_separator, None)
        d["a.b.c"] = 1
        with self.assertRaises(ValueError):
            d.keypath_separator = "."
        d.keypath_separator = "/"
        self.assertEqual(d.keypath_separator, "/")
        d["x/y/z"] = 2
        r = {
            "a.b.c": 1,
            "x": {
                "y": {
                    "z": 2,
                },
            },
        }
        self.assertEqual(d, r)

    def test_set_override_existing_item(self):
        d = {}
        b = KeypathDict(d)
        b.set("a.b.c", 1)
        r = {"a": {"b": {"c": 1}}}
        b.set("a.b.c", 2)
        r = {"a": {"b": {"c": 2}}}
        self.assertEqual(b, r)
        b.set("a.b.c.d", 3)
        r = {"a": {"b": {"c": {"d": 3}}}}
        self.assertEqual(b, r)

    def test_setitem_override_existing_item(self):
        d = {}
        b = KeypathDict(d)
        b["a.b.c"] = 1
        r = {"a": {"b": {"c": 1}}}
        b["a.b.c"] = 2
        r = {"a": {"b": {"c": 2}}}
        self.assertEqual(b, r)
        b["a.b.c.d"] = 3
        r = {"a": {"b": {"c": {"d": 3}}}}
        self.assertEqual(b, r)

    def test_setitem_with_keys_list(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d)
        b["a", "b.c"] = 2
        self.assertEqual(b["a.b.c"], 2)
        b["a", "b", "c"] = 3
        self.assertEqual(b["a.b.c"], 3)
        b["a", "b", "d"] = 4
        self.assertEqual(b["a.b.d"], 4)
        b["a", "b", "e"] = 5
        self.assertEqual(b["a.b.e"], 5)

    def test_setitem_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d, keypath_separator=None)
        b["a", "b", "c"] = 3
        with self.assertRaises(KeyError):
            val = b["a.b.c"]
            # print(val)
        self.assertEqual(b["a", "b", "c"], 3)

        b["a", "b", "d"] = 4
        with self.assertRaises(KeyError):
            val = b["a.b.d"]
            # print(val)
        self.assertEqual(b["a", "b", "d"], 4)

        b["a", "b", "e"] = 5
        with self.assertRaises(KeyError):
            val = b["a.b.e"]
            # print(val)
        self.assertEqual(b["a", "b", "e"], 5)

    def test_setitem_with_dict_value_with_separator_in_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            },
        }
        b = KeypathDict(d)
        v = {
            "i.j.k": 3,
            "x.y.z": 4,
        }
        # print(b['a.b.e.x.y.z'])
        # print(b.keypaths())
        with self.assertRaises(ValueError):
            b["a.b.e"] = v

    def test_delitem_with_1_valid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        del b["a"]
        with self.assertRaises(KeyError):
            del b["a"]
        self.assertEqual(b.get("a"), None)

    def test_delitem_with_1_invalid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["b"]
        self.assertEqual(b.get("b"), None)

    def test_delitem_with_2_valid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)

        del b["a.b"]
        with self.assertRaises(KeyError):
            del b["a.b"]
        self.assertEqual(b.get("a"), {})

        del b["a"]
        with self.assertRaises(KeyError):
            del b["a"]
        self.assertEqual(b.get("a"), None)

    def test_delitem_with_2_invalid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["a.c"]
        self.assertEqual(b.get("a"), {"b": 1})

    def test_delitem_with_3_valid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            }
        }
        b = KeypathDict(d)

        del b["a.b.c"]
        with self.assertRaises(KeyError):
            del b["a.b.c"]
        self.assertEqual(b.get("a.b"), {"d": 2})

        del b["a.b.d"]
        with self.assertRaises(KeyError):
            del b["a.b.d"]
        self.assertEqual(b.get("a.b"), {})

        del b["a.b"]
        with self.assertRaises(KeyError):
            del b["a.b"]
        self.assertEqual(b.get("a.b"), None)

    def test_delitem_with_3_invalid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["a.b.c.d"]
        self.assertEqual(b.get("a.b.c"), 1)

    def test_delitem_with_keys_list(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b["a", "b", "c", "d"]
        del b["a", "b", "c"]
        self.assertEqual(b.get("a.b.c", 3), 3)

    def test_delitem_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
            }
        }
        b = KeypathDict(d, keypath_separator=None)
        with self.assertRaises(KeyError):
            del b["a", "b", "c", "d"]
        del b["a", "b", "c"]
        self.assertEqual(b.get("a.b.c", 3), 3)

    def test_pop_default(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        val = b.pop("a", 2)
        self.assertEqual(val, 1)
        val = b.pop("b", 2)
        self.assertEqual(val, 2)
        val = b.pop("c", 3)
        self.assertEqual(val, 3)

    def test_pop_with_1_valid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        val = b.pop("a")
        self.assertEqual(val, 1)

    def test_pop_with_1_invalid_key(self):
        d = {
            "a": 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b.pop("b")
        val = b.pop("b", False)
        self.assertFalse(val)
        val = b.pop("b", None)
        self.assertEqual(val, None)

    def test_pop_with_2_valid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)

        val = b.pop("a.b")
        with self.assertRaises(KeyError):
            val = b.pop("a.b")
        self.assertEqual(val, 1)

        val = b.pop("a")
        with self.assertRaises(KeyError):
            val = b.pop("a")
        self.assertEqual(val, {})

    def test_pop_with_2_invalid_keys(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)

        val = b.pop("a.c", 2)
        self.assertEqual(val, 2)
        with self.assertRaises(KeyError):
            val = b.pop("a.c")
        self.assertEqual(b.get("a"), {"b": 1})

        val = b.pop("x.y", 1)
        self.assertEqual(val, 1)
        with self.assertRaises(KeyError):
            val = b.pop("x.y")

    def test_pop_with_keys_list(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d)

        val = b.pop(["a", "c"], 2)
        self.assertEqual(val, 2)
        with self.assertRaises(KeyError):
            val = b.pop(["a", "c"])
        self.assertEqual(b.get("a"), {"b": 1})

        val = b.pop(["x", "y"], 1)
        self.assertEqual(val, 1)
        with self.assertRaises(KeyError):
            val = b.pop(["x", "y"])

        val = b.pop(["a", "b"])
        self.assertEqual(val, 1)

    def test_pop_with_keys_list_and_no_keypath_separator(self):
        d = {
            "a": {
                "b": 1,
            }
        }
        b = KeypathDict(d, keypath_separator=None)

        val = b.pop(["a", "c"], 2)
        self.assertEqual(val, 2)
        with self.assertRaises(KeyError):
            val = b.pop(["a", "c"])
        self.assertEqual(b.get("a"), {"b": 1})

        val = b.pop(["x", "y"], 1)
        self.assertEqual(val, 1)
        with self.assertRaises(KeyError):
            val = b.pop(["x", "y"])

        val = b.pop(["a", "b"])
        self.assertEqual(val, 1)

    def test_setdefault_with_1_key(self):
        d = {
            "a": None,
            "b": 0,
            "c": 1,
        }
        b = KeypathDict(d)
        b.setdefault("a", 2)
        b.setdefault("b", 2)
        b.setdefault("c", 2)
        b.setdefault("d", 2)
        self.assertEqual(b["a"], None)
        self.assertEqual(b["b"], 0)
        self.assertEqual(b["c"], 1)
        self.assertEqual(b["d"], 2)

    def test_setdefault_with_2_keys(self):
        d = {
            "x": {
                "a": None,
                "b": 0,
                "c": 1,
            },
        }
        b = KeypathDict(d)
        b.setdefault("x.a", 2)
        b.setdefault("x.b", 2)
        b.setdefault("x.c", 2)
        b.setdefault("x.d", 2)
        self.assertEqual(b["x.a"], None)
        self.assertEqual(b["x.b"], 0)
        self.assertEqual(b["x.c"], 1)
        self.assertEqual(b["x.d"], 2)

    def test_setdefault_with_3_keys(self):
        d = {
            "y": {
                "z": {
                    "a": None,
                    "b": 0,
                    "c": 1,
                },
            },
        }
        b = KeypathDict(d)
        b.setdefault("y.z.a", 2)
        b.setdefault("y.z.b", 2)
        b.setdefault("y.z.c", 2)
        b.setdefault("y.z.d", 2)
        self.assertEqual(b["y.z.a"], None)
        self.assertEqual(b["y.z.b"], 0)
        self.assertEqual(b["y.z.c"], 1)
        self.assertEqual(b["y.z.d"], 2)
