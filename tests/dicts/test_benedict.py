import re
import unittest
from datetime import datetime
from decimal import Decimal

from benedict import benedict


class benedict_test_case(unittest.TestCase):
    """
    This class describes a benedict test case.
    """

    def test_clean(self):
        d = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "g": None,
            "h": "0",
        }
        bd = benedict(d.copy())
        bd.clean()
        r = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }
        self.assertEqual(bd, r)

        bd = benedict(d.copy())
        bd.clean(collections=False)
        r = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "h": "0",
        }
        self.assertEqual(bd, r)

        bd = benedict(d.copy())
        bd.clean(strings=False)
        r = {
            "b": {"x": 1},
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "h": "0",
        }
        self.assertEqual(bd, r)

    def test_clone(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d)
        c = b.clone()
        self.assertEqual(type(b), type(c))
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c["a"]["b"]["c"] = 2
        self.assertEqual(b["a"]["b"]["c"], 1)
        self.assertEqual(c["a"]["b"]["c"], 2)

    def test_copy(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d)
        c = b.copy()
        self.assertEqual(type(b), type(c))
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c["a.b.c"] = 2
        self.assertEqual(b.get("a.b.c"), 2)
        self.assertEqual(c.get("a.b.c"), 2)

    def test_copy_with_custom_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d, keypath_separator="/")
        c = b.copy()
        self.assertEqual(c.keypath_separator, "/")

    def test_deepcopy(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d)
        c = b.deepcopy()
        self.assertEqual(type(b), type(c))
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c["a.b.c"] = 2
        self.assertEqual(b.get("a.b.c"), 1)
        self.assertEqual(c.get("a.b.c"), 2)

    def test_deepcopy_with_custom_keypath_separator(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d, keypath_separator="/")
        c = b.deepcopy()
        self.assertEqual(c.keypath_separator, "/")

    def test_deepupdate_with_single_dict(self):
        d = {
            "a": 1,
            "b": 1,
        }
        a = {
            "b": 2,
            "c": 3,
        }
        bd = benedict(d)
        bd.deepupdate(a)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        self.assertEqual(bd, r)

    def test_deepupdate_with_multiple_dicts(self):
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
        bd = benedict(d)
        bd.deepupdate(a, b, c)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        self.assertEqual(bd, r)

    def test_deepupdate(self):
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
        a = {
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
        bd = benedict(d)
        bd.deepupdate(a)
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
        self.assertEqual(bd, r)

    def test_dump(self):
        d = {
            "a": {
                "b": {
                    "c": 1,
                }
            }
        }
        b = benedict(d)
        expected_output = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        output = benedict.dump(b)
        self.assertEqual(output, expected_output)
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_datetime(self):
        d = {
            "datetime": datetime(2019, 6, 11),
        }
        b = benedict(d)
        expected_output = """{
    "datetime": "2019-06-11T00:00:00"
}"""
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_decimal(self):
        d = {
            "decimal": Decimal("1.75"),
        }
        b = benedict(d)
        expected_output = """{
    "decimal": "1.75"
}"""
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_filter(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        b = benedict(d)
        with self.assertRaises(ValueError):
            f = b.filter(True)
        f = b.filter(lambda key, val: isinstance(val, int))
        r = {
            "a": 1,
            "b": 2,
            "f": 6,
            "g": 7,
        }
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f, r)
        self.assertFalse(b is f)

    def test_filter_with_custom_keypath_separator(self):
        d = {
            "a.b": 1,
            "b.c": 2,
            "c.d": 3,
            "e.f": "4",
            "f.g": "5",
        }
        b = benedict(d, keypath_separator="/")
        f = b.filter(lambda key, val: isinstance(val, int))
        r = {
            "a.b": 1,
            "b.c": 2,
            "c.d": 3,
        }
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f, r)
        self.assertFalse(b is f)
        self.assertEqual(b.keypath_separator, f.keypath_separator)

    def test_filter_with_parse(self):
        d = {
            "a": {
                "ok": "yes",
            },
            "b": {
                "ok": "no",
            },
            "c": {
                "ok": "yes",
            },
            "e": {
                "ok": "no",
            },
            "f": {
                "ok": "yes",
            },
            "g": {
                "ok": "no",
            },
        }
        b = benedict(d)
        f = b.filter(lambda key, val: benedict(val).get_bool("ok"))
        r = {
            "a": {
                "ok": "yes",
            },
            "c": {
                "ok": "yes",
            },
            "f": {
                "ok": "yes",
            },
        }
        self.assertEqual(f, r)
        self.assertTrue(isinstance(f, benedict))

    def test_filter(self):
        d = {
            "a": 1,
            "b": 2,
            "c": {
                "d": {
                    "e": 3,
                    "f": 4,
                }
            },
        }
        b = benedict(d)
        r = b.find(["x.y.z", "a.b.c", "c.d.e"])
        self.assertEqual(r, 3)

    def test_flatten(self):
        d = {
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
        b = benedict(d)
        f = b.flatten()
        r = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        self.assertEqual(f, r)
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))

    def test_flatten_with_custom_keypath_separator(self):
        d = {
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
        b = benedict(d, keypath_separator="/")
        f = b.flatten()
        r = {
            "a": 1,
            "b": 2,
            "c_d_e": 3,
            "c_d_f": 4,
            "c_d_g_h": 5,
        }
        self.assertEqual(f, r)
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(b.keypath_separator, f.keypath_separator)

    def test_flatten_with_custom_separator(self):
        d = {
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
        b = benedict(d)
        f = b.flatten(separator="|")
        r = {
            "a": 1,
            "b": 2,
            "c|d|e": 3,
            "c|d|f": 4,
            "c|d|g|h": 5,
        }
        self.assertEqual(f, r)
        self.assertFalse(b is f)

    def test_flatten_with_key_conflict(self):
        d = {
            "a": 1,
            "b": 2,
            "c_d": 4,
            "c": {
                "d": 3,
            },
        }
        b = benedict(d)
        with self.assertRaises(KeyError):
            f = b.flatten()
        # r = {
        #     'a': 1,
        #     'b': 2,
        #     'c_d': 4,
        # }
        # self.assertEqual(f, r)
        # self.assertFalse(b is f)

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
        b = benedict.fromkeys(k)
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
        self.assertEqual(type(b), benedict)

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
        b = benedict.fromkeys(k, True)
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
        self.assertEqual(type(b), benedict)

    def test_from_base64(self):
        j = "eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9"
        # static method
        d = benedict.from_base64(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )
        # static method with subformat
        d = benedict.from_base64(j, subformat="json")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )
        # constructor
        d = benedict(j, format="base64")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )
        # constructor with subformat
        d = benedict(j, format="base64", subformat="json")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )

    def test_from_csv_with_valid_data(self):
        s = """id,name,age,height,weight
1,Alice,20,62,120.6
2,Freddie,21,74,190.6
3,Bob,17,68,120.0
4,François,32,75,110.05
"""
        r = {
            "values": [
                {
                    "id": "1",
                    "name": "Alice",
                    "age": "20",
                    "height": "62",
                    "weight": "120.6",
                },
                {
                    "id": "2",
                    "name": "Freddie",
                    "age": "21",
                    "height": "74",
                    "weight": "190.6",
                },
                {
                    "id": "3",
                    "name": "Bob",
                    "age": "17",
                    "height": "68",
                    "weight": "120.0",
                },
                {
                    "id": "4",
                    "name": "François",
                    "age": "32",
                    "height": "75",
                    "weight": "110.05",
                },
            ],
        }
        # static method
        d = benedict.from_csv(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = benedict(s, format="csv")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_json(self):
        j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = benedict.from_json(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )
        # constructor
        d = benedict(j, format="json")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
            },
        )

    def test_from_query_string_with_valid_data(self):
        s = "ok=1&test=2&page=3&lib=python%20benedict&author=Fabio+Caccamo&author=Fabio%20Caccamo"
        r = {
            "ok": "1",
            "test": "2",
            "page": "3",
            "lib": "python benedict",
            "author": "Fabio Caccamo",
        }
        # static method
        d = benedict.from_query_string(s)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, r)
        # constructor
        d = benedict(s, format="query-string")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, r)

    def test_from_toml(self):
        j = """
            a = 1

            [b]
            c = 3
            d = 4
        """
        # static method
        d = benedict.from_toml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )
        # constructor
        d = benedict(j, format="toml")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )

    def test_from_yaml_with_keypath_separator_in_keys(self):
        # fix: https://github.com/fabiocaccamo/python-benedict/issues/12
        j = """
192.168.0.1:
  test: value
  test2: value2
value:
  value_with_period: 12.34.45
"""
        with self.assertRaises(ValueError):
            # static method
            d = benedict.from_yaml(j)
            self.assertTrue(isinstance(d, dict))
            self.assertEqual(
                d,
                {
                    "a": 1,
                    "b": {
                        "c": 3,
                        "d": 4,
                    },
                },
            )
            # constructor
            d = benedict(j, format="yaml")
            self.assertTrue(isinstance(d, dict))
            self.assertEqual(
                d,
                {
                    "a": 1,
                    "b": {
                        "c": 3,
                        "d": 4,
                    },
                },
            )
        r = {
            "192.168.0.1": {
                "test": "value",
                "test2": "value2",
            },
            "value": {
                "value_with_period": "12.34.45",
            },
        }
        # static method
        d = benedict.from_yaml(j, keypath_separator=None)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = benedict(j, format="yaml", keypath_separator=None)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_xml(self):
        j = """
<?xml version="1.0" ?>
<root>
    <a>1</a>
    <b>
        <c>3</c>
        <d>4</d>
    </b>
</root>
"""
        # static method
        d = benedict.from_xml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d.get("root"),
            {
                "a": "1",
                "b": {
                    "c": "3",
                    "d": "4",
                },
            },
        )
        # constructor
        d = benedict(j, format="xml")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d.get("root"),
            {
                "a": "1",
                "b": {
                    "c": "3",
                    "d": "4",
                },
            },
        )

    def test_from_yaml(self):
        j = """
a: 1
b:
  c: 3
  d: 4
"""
        # static method
        d = benedict.from_yaml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )
        # constructor
        d = benedict(j, format="yaml")
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )

    def test_get(self):
        d = {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": 3,
                },
            },
        }
        b = benedict(d)
        self.assertEqual(b.get("a"), 1)
        self.assertEqual(b.get("b.c"), 2)
        # self.assertTrue(isinstance(b.get('b'), benedict))
        # self.assertTrue(isinstance(b.get('b.d'), benedict))
        # bb = b.get('b')
        # self.assertTrue(isinstance(bb.get('d'), benedict))

    def test_get_item(self):
        d = {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": 3,
                },
            },
        }
        b = benedict(d)
        self.assertEqual(b["a"], 1)
        self.assertEqual(b["b.c"], 2)
        # self.assertTrue(isinstance(b['b'], benedict))
        # self.assertTrue(isinstance(b['b.d'], benedict))
        # bb = b['b']
        # self.assertTrue(isinstance(bb['d'], benedict))

    def test_get_dict(self):
        d = {
            "a": {
                "x": 1,
                "y": 2,
            },
            "b": {},
        }
        b = benedict(d)
        # self.assertTrue(isinstance(b.get_dict('a'), benedict))
        self.assertEqual(b.get("a.x"), 1)

    def test_get_list(self):
        d = {
            "a": [
                {
                    "b": {
                        "c": 1,
                    }
                },
                {
                    "b": {
                        "c": 2,
                    }
                },
                {
                    "b": {
                        "c": 3,
                    }
                },
            ]
        }
        b = benedict(d)
        l = b.get_list("a")
        # self.assertTrue(isinstance(l[0], benedict))
        # self.assertTrue(isinstance(l[1], benedict))
        # self.assertTrue(isinstance(l[2], benedict))
        # self.assertEqual(l[0].get('b.c'), 1)
        # self.assertEqual(l[1].get('b.c'), 2)
        # self.assertEqual(l[2].get('b.c'), 3)
        self.assertEqual(benedict(l[0]).get("b.c"), 1)
        self.assertEqual(benedict(l[1]).get("b.c"), 2)
        self.assertEqual(benedict(l[2]).get("b.c"), 3)

    def test_get_list_item(self):
        d = {
            "a": [
                {
                    "b": {
                        "c": 1,
                    }
                },
                {
                    "b": {
                        "c": 2,
                    }
                },
                {
                    "b": {
                        "c": 3,
                    }
                },
            ]
        }
        b = benedict(d)
        i = benedict(b.get_list_item("a", index=1))
        # self.assertTrue(isinstance(i, benedict))
        self.assertEqual(i.get("b.c"), 2)

    def test_get_phonenumber(self):
        d = {
            "a": {
                "b": " (0039) 3334445566 ",
                "c": "+393334445566  ",
                "d": "+39333444556677889900",
            }
        }
        r = {
            "e164": "+393334445566",
            "international": "+39 333 444 5566",
            "national": "333 444 5566",
        }
        b = benedict(d)

        p = b.get_phonenumber("a.b")
        self.assertEqual(p, r)
        # self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber("a.c")
        self.assertEqual(p, r)
        # self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber("a.d")
        self.assertEqual(p, {})
        # self.assertTrue(isinstance(p, benedict))

    def test_groupby(self):
        d = {
            "cities": [
                {
                    "country_code": "IT",
                    "name": "Torino",
                },
                {
                    "country_code": "DE",
                    "name": "Berlin",
                },
                {
                    "country_code": "IT",
                    "name": "Milano",
                },
                {
                    "country_code": "FR",
                    "name": "Paris",
                },
                {
                    "country_code": "IT",
                    "name": "Venezia",
                },
                {
                    "country_code": "IT",
                    "name": "Roma",
                },
                {
                    "country_code": "FR",
                    "name": "Lyon",
                },
                {
                    "country_code": "IT",
                    "name": "Napoli",
                },
                {
                    "country_code": "DE",
                    "name": "Munich",
                },
                {
                    "country_code": "IT",
                    "name": "Palermo",
                },
            ],
        }
        bd = benedict(d)
        bd_cities = bd["cities"]
        g = bd.groupby("cities", "country_code")

        self.assertEqual(len(g), 3)
        self.assertTrue("IT" in g)
        self.assertTrue("FR" in g)
        self.assertTrue("DE" in g)

        self.assertEqual(len(g["IT"]), 6)
        self.assertTrue(bd_cities[0] in g["IT"])
        self.assertTrue(bd_cities[2] in g["IT"])
        self.assertTrue(bd_cities[4] in g["IT"])
        self.assertTrue(bd_cities[5] in g["IT"])
        self.assertTrue(bd_cities[7] in g["IT"])
        self.assertTrue(bd_cities[9] in g["IT"])

        self.assertEqual(len(g["FR"]), 2)
        self.assertTrue(bd_cities[3] in g["FR"])
        self.assertTrue(bd_cities[6] in g["FR"])

        self.assertEqual(len(g["DE"]), 2)
        self.assertTrue(bd_cities[1] in g["DE"])
        self.assertTrue(bd_cities[8] in g["DE"])

    def test_invert(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        bd = benedict(d)
        i = bd.invert()
        r = {
            1: ["a"],
            2: ["b"],
            3: ["c"],
            4: ["d"],
            5: ["e"],
        }
        self.assertEqual(i, r)

    def test_invert_with_custom_keypath_separator(self):
        d = {
            "a": "1.0",
            "b": "2.0",
            "c": "3.0",
            "d": "4.0",
            "e": "5.0",
        }
        bd = benedict(d, keypath_separator="/")
        i = bd.invert()
        r = {
            "1.0": ["a"],
            "2.0": ["b"],
            "3.0": ["c"],
            "4.0": ["d"],
            "5.0": ["e"],
        }
        self.assertEqual(i, r)
        self.assertEqual(bd.keypath_separator, i.keypath_separator)

    def test_invert_multiple_values(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 1,
            "e": 2,
            "f": 3,
        }
        bd = benedict(d)
        i = bd.invert()
        self.assertTrue("a" and "d" in i[1])
        self.assertTrue("b" and "e" in i[2])
        self.assertTrue("c" and "f" in i[3])

    def test_invert_flat(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        bd = benedict(d)
        i = bd.invert(flat=True)
        r = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
        }
        self.assertEqual(i, r)

    def test_items_sorted_by_keys(self):
        d = {
            "y": 3,
            "a": 6,
            "f": 9,
            "z": 4,
            "x": 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_keys()
        self.assertEqual(
            items,
            [
                ("a", 6),
                ("f", 9),
                ("x", 1),
                ("y", 3),
                ("z", 4),
            ],
        )

    def test_items_sorted_by_keys_reverse(self):
        d = {
            "y": 3,
            "a": 6,
            "f": 9,
            "z": 4,
            "x": 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_keys(reverse=True)
        self.assertEqual(
            items,
            [
                ("z", 4),
                ("y", 3),
                ("x", 1),
                ("f", 9),
                ("a", 6),
            ],
        )

    def test_items_sorted_by_values(self):
        d = {
            "a": 3,
            "b": 6,
            "c": 9,
            "e": 4,
            "d": 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_values()
        self.assertEqual(
            items,
            [
                ("d", 1),
                ("a", 3),
                ("e", 4),
                ("b", 6),
                ("c", 9),
            ],
        )

    def test_items_sorted_by_values_reverse(self):
        d = {
            "a": 3,
            "b": 6,
            "c": 9,
            "e": 4,
            "d": 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_values(reverse=True)
        self.assertEqual(
            items,
            [
                ("c", 9),
                ("b", 6),
                ("e", 4),
                ("a", 3),
                ("d", 1),
            ],
        )

    def test_keypaths(self):
        d = {
            "x": {
                "y": True,
                "z": False,
            },
            "a": {
                "b": {
                    "c": 0,
                    "d": None,
                    "e": {},
                    "f": [1, 2, 3, 4, 5],
                },
            },
        }
        b = benedict(d)
        r = [
            "a",
            "a.b",
            "a.b.c",
            "a.b.d",
            "a.b.e",
            "a.b.f",
            "x",
            "x.y",
            "x.z",
        ]
        self.assertEqual(b.keypaths(), r)
        r = [
            "a",
            "a.b",
            "a.b.c",
            "a.b.d",
            "a.b.e",
            "a.b.f",
            "a.b.f[0]",
            "a.b.f[1]",
            "a.b.f[2]",
            "a.b.f[3]",
            "a.b.f[4]",
            "x",
            "x.y",
            "x.z",
        ]
        self.assertEqual(b.keypaths(indexes=True), r)

    def test_match_with_regex_pattern(self):
        d = {
            "results": [
                {
                    "name_1": "A",
                },
                {
                    "name_2": "B",
                },
                {
                    "name_3": "C",
                },
                {
                    "name_X": "D",
                },
            ],
        }
        b = benedict(d)
        r = re.compile(r"results\[[\d]+\].name_[\d]+")
        m = b.match(r)
        self.assertEqual(m, ["A", "B", "C"])

    def test_match_with_regex_pattern_and_custom_keypath_separator(self):
        d = {
            "results": [
                {
                    "name_1": "A",
                },
                {
                    "name_2": "B",
                },
                {
                    "name_3": "C",
                },
                {
                    "name_X": "D",
                },
            ],
        }
        b = benedict(d, keypath_separator="/")
        r = re.compile(r"results\[[\d]+\]/name_[\d]+")
        m = b.match(r)
        self.assertEqual(m, ["A", "B", "C"])

    def test_match_with_string_pattern(self):
        d = {
            "results": [
                {
                    "name": "A",
                    "props": [1, 2, 3],
                },
                {
                    "name": "B",
                    "props": [4, 5, 6],
                },
                {
                    "name": "C",
                    "props": [7, 8, 9],
                },
            ],
        }
        b = benedict(d)
        m = b.match("results[*].name")
        self.assertEqual(m, ["A", "B", "C"])
        m = b.match("results[*].props[0]")
        self.assertEqual(m, [1, 4, 7])
        m = b.match("results[*].props[1]")
        self.assertEqual(m, [2, 5, 8])
        m = b.match("results[*].props[2]")
        self.assertEqual(m, [3, 6, 9])

    def test_match_with_string_pattern_and_custom_keypath_separator(self):
        d = {
            "results": [
                {
                    "name": "A",
                    "props": [1, 2, 3],
                },
                {
                    "name": "B",
                    "props": [4, 5, 6],
                },
                {
                    "name": "C",
                    "props": [7, 8, 9],
                },
            ],
        }
        b = benedict(d, keypath_separator="/")
        m = b.match("results[*]/name")
        self.assertEqual(m, ["A", "B", "C"])
        m = b.match("results[*]/props[2]")
        self.assertEqual(m, [3, 6, 9])

    def test_merge_with_single_dict(self):
        d = {
            "a": 1,
            "b": 1,
        }
        a = {
            "b": 2,
            "c": 3,
        }
        d = benedict(d)
        d.merge(a)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
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
        d = benedict(d)
        d.merge(a, b, c)
        r = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
        }
        self.assertEqual(d, r)

    def test_merge(self):
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
        a = {
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
        d = benedict(d)
        d.merge(a)
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

    def test_move(self):
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
        b = benedict(d)
        b.move("a", "c.z")
        r = {
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 3,
                "y": 3,
                "z": {
                    "x": 1,
                    "y": 1,
                },
            },
        }
        self.assertEqual(b, r)

    def test_nest(self):
        d = {
            "values": [
                {"id": 1, "parent_id": None, "name": "John"},
                {"id": 2, "parent_id": 1, "name": "Frank"},
                {"id": 3, "parent_id": 2, "name": "Tony"},
                {"id": 4, "parent_id": 3, "name": "Jimmy"},
                {"id": 5, "parent_id": 1, "name": "Sam"},
                {"id": 6, "parent_id": 3, "name": "Charles"},
                {"id": 7, "parent_id": 2, "name": "Bob"},
                {"id": 8, "parent_id": 3, "name": "Paul"},
                {"id": 9, "parent_id": None, "name": "Michael"},
            ],
        }
        bd = benedict(d)
        n = bd.nest("values")
        r = [
            {
                "id": 1,
                "parent_id": None,
                "name": "John",
                "children": [
                    {
                        "id": 2,
                        "parent_id": 1,
                        "name": "Frank",
                        "children": [
                            {
                                "id": 3,
                                "parent_id": 2,
                                "name": "Tony",
                                "children": [
                                    {
                                        "id": 4,
                                        "parent_id": 3,
                                        "name": "Jimmy",
                                        "children": [],
                                    },
                                    {
                                        "id": 6,
                                        "parent_id": 3,
                                        "name": "Charles",
                                        "children": [],
                                    },
                                    {
                                        "id": 8,
                                        "parent_id": 3,
                                        "name": "Paul",
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "id": 7,
                                "parent_id": 2,
                                "name": "Bob",
                                "children": [],
                            },
                        ],
                    },
                    {
                        "id": 5,
                        "parent_id": 1,
                        "name": "Sam",
                        "children": [],
                    },
                ],
            },
            {
                "id": 9,
                "parent_id": None,
                "name": "Michael",
                "children": [],
            },
        ]
        self.assertEqual(n, r)

    def test_nest_with_custom_keys(self):
        d = {
            "values": [
                {"ID": 1, "PARENT": None, "name": "John"},
                {"ID": 2, "PARENT": 1, "name": "Frank"},
                {"ID": 3, "PARENT": 2, "name": "Tony"},
                {"ID": 4, "PARENT": 3, "name": "Jimmy"},
                {"ID": 5, "PARENT": 1, "name": "Sam"},
                {"ID": 6, "PARENT": 3, "name": "Charles"},
                {"ID": 7, "PARENT": 2, "name": "Bob"},
                {"ID": 8, "PARENT": 3, "name": "Paul"},
                {"ID": 9, "PARENT": None, "name": "Michael"},
            ],
        }
        bd = benedict(d)
        n = bd.nest("values", "ID", "PARENT", "CHILDREN")
        r = [
            {
                "ID": 1,
                "PARENT": None,
                "name": "John",
                "CHILDREN": [
                    {
                        "ID": 2,
                        "PARENT": 1,
                        "name": "Frank",
                        "CHILDREN": [
                            {
                                "ID": 3,
                                "PARENT": 2,
                                "name": "Tony",
                                "CHILDREN": [
                                    {
                                        "ID": 4,
                                        "PARENT": 3,
                                        "name": "Jimmy",
                                        "CHILDREN": [],
                                    },
                                    {
                                        "ID": 6,
                                        "PARENT": 3,
                                        "name": "Charles",
                                        "CHILDREN": [],
                                    },
                                    {
                                        "ID": 8,
                                        "PARENT": 3,
                                        "name": "Paul",
                                        "CHILDREN": [],
                                    },
                                ],
                            },
                            {
                                "ID": 7,
                                "PARENT": 2,
                                "name": "Bob",
                                "CHILDREN": [],
                            },
                        ],
                    },
                    {
                        "ID": 5,
                        "PARENT": 1,
                        "name": "Sam",
                        "CHILDREN": [],
                    },
                ],
            },
            {
                "ID": 9,
                "PARENT": None,
                "name": "Michael",
                "CHILDREN": [],
            },
        ]
        self.assertEqual(n, r)

    def test_pop(self):
        d = {
            "a": 1,
            "b": {
                "c": 2,
                "d": {
                    "e": 3,
                },
            },
        }
        b = benedict(d)
        self.assertEqual(b.pop("a"), 1)
        self.assertEqual(b.pop("b.c"), 2)
        # self.assertTrue(isinstance(b.pop('b.d'), benedict))

    def test_remove_with_key(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
        }
        b = benedict(d)
        b.remove("c")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keys_list(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        b = benedict(d)
        b.remove(["c", "e", "f", "g", "x", "y", "z"])
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keys_args(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        b = benedict(d)
        b.remove("c", "e", "f", "g", "x", "y", "z")
        r = {
            "a": 1,
            "b": 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keypath(self):
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
            "d": {
                "x": 4,
                "y": 4,
            },
        }
        b = benedict(d)
        b.remove(["a.x", "b.y", "c.x", "c.y", "d"])
        r = {
            "a": {"y": 1},
            "b": {"x": 2},
            "c": {},
        }
        self.assertEqual(b, r)

    def test_rename(self):
        d = {
            "a": {
                "x": 1,
                "y": 1,
            },
            "b": {
                "x": 2,
                "y": 2,
            },
        }
        b = benedict(d)
        b.rename("a.x", "a.xx")
        b.rename("a.y", "a.yy")
        b.rename("a", "aa")
        r = {
            "aa": {
                "xx": 1,
                "yy": 1,
            },
            "b": {
                "x": 2,
                "y": 2,
            },
        }
        self.assertEqual(b, r)
        with self.assertRaises(KeyError):
            b.rename("aa", "b")

    def test_search(self):
        d = {
            "a": "Hello world",
            "b": "Hello world!",
            "c": {
                "d": True,
                "e": " hello world ",
                "f": {
                    "g": "HELLO",
                    "h": 12345,
                    "hello": True,
                },
            },
            "Hello world": "Hello World",
        }
        b = benedict(d)

        results = b.search(
            "Hello", in_keys=False, in_values=False, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

        results = b.search(
            "Hello", in_keys=False, in_values=True, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

        results = b.search(
            "Hello", in_keys=False, in_values=True, exact=True, case_sensitive=False
        )
        self.assertEqual(len(results), 1)
        self.assertTrue(
            (
                d["c"]["f"],
                "g",
                d["c"]["f"]["g"],
            )
            in results
        )

        results = b.search(
            "hello", in_keys=True, in_values=True, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 6)
        self.assertTrue(
            (
                d,
                "a",
                d["a"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "b",
                d["b"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"],
                "e",
                d["c"]["e"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"]["f"],
                "g",
                d["c"]["f"]["g"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"]["f"],
                "hello",
                d["c"]["f"]["hello"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "Hello world",
                d["Hello world"],
            )
            in results
        )

        results = b.search(
            "hello", in_keys=True, in_values=False, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 2)
        self.assertTrue(
            (
                d["c"]["f"],
                "hello",
                d["c"]["f"]["hello"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "Hello world",
                d["Hello world"],
            )
            in results
        )

    # def test_setdefault(self):
    #     d = {
    #         'a': 1,
    #         'b': {
    #             'c': 2,
    #             'd': {
    #                 'e': 3,
    #             }
    #         }
    #     }
    #     b = benedict(d)
    #     self.assertTrue(isinstance(b.setdefault('b', 1), benedict))
    #     self.assertTrue(isinstance(b.setdefault('b.d', 1), benedict))

    def test_standardize(self):
        d = {
            "CamelCase": 1,
            "CamelCamelCase": 1,
            "Camel2Camel2Case": 1,
            "getHTTPResponseCode": 1,
            "get2HTTPResponseCode": 1,
            "HTTPResponseCode": 1,
            "HTTPResponseCodeXYZ": 1,
            " LocationCoordinates ": {
                "Lat. ": 0.0,
                "Lng. ": 0.0,
            },
        }
        b = benedict(d, keypath_separator=None)
        b.standardize()
        b.keypath_separator = "."
        r = {
            "camel_case": 1,
            "camel_camel_case": 1,
            "camel2_camel2_case": 1,
            "get_http_response_code": 1,
            "get2_http_response_code": 1,
            "http_response_code": 1,
            "http_response_code_xyz": 1,
            "location_coordinates": {
                "lat": 0.0,
                "lng": 0.0,
            },
        }
        self.assertEqual(b, r)
        self.assertEqual(b["location_coordinates.lat"], 0.0)
        self.assertEqual(b["location_coordinates.lng"], 0.0)

    def test_subset(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        b = benedict(d)
        f = b.subset(["c", "f", "x"])
        r = {
            "c": "4",
            "f": 6,
            "x": None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))

    def test_subset_with_custom_keypath_separator(self):
        d = {
            "a.x": 1,
            "b.x": 2,
            "c.x": "4",
            "e.x": "5",
            "f.x": 6,
            "g.x": 7,
        }
        b = benedict(d, keypath_separator="/")
        f = b.subset(["c.x", "f.x", "x.x"])
        r = {
            "c.x": "4",
            "f.x": 6,
            "x.x": None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertEqual(type(b), type(f))
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(b.keypath_separator, f.keypath_separator)

    def test_subset_with_keys_args(self):
        d = {
            "a": 1,
            "b": 2,
            "c": "4",
            "e": "5",
            "f": 6,
            "g": 7,
        }
        b = benedict(d)
        f = b.subset("c", "f", "x")
        r = {
            "c": "4",
            "f": 6,
            "x": None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)

    def test_subset_with_keypath(self):
        d = {
            "x": {
                "a": 1,
                "aa": 1,
            },
            "y": {
                "b": 2,
                "bb": 2,
            },
            "z": {
                "c": 3,
                "cc": 3,
            },
        }
        b = benedict(d)
        f = b.subset(["x", "y"])
        r = {
            "x": {
                "a": 1,
                "aa": 1,
            },
            "y": {
                "b": 2,
                "bb": 2,
            },
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f.get("x.a"), 1)
        self.assertEqual(f.get("x.aa"), 1)
        self.assertEqual(f.get("y.b"), 2)
        self.assertEqual(f.get("y.bb"), 2)
        # test with keypath
        f = b.subset(["x.a", "y.b"])
        r = {
            "x": {
                "a": 1,
            },
            "y": {
                "b": 2,
            },
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f.get("x.a"), 1)
        self.assertEqual(f.get("y.b"), 2)

    def test_swap(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = benedict(d)
        b.swap("a", "b")
        r = {
            "a": 2,
            "b": 1,
            "c": 3,
        }
        self.assertEqual(b, r)

    def test_swap_with_invalid_key(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = benedict(d)
        with self.assertRaises(KeyError):
            b.swap("a", "d")

    def test_swap_with_keypath(self):
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
        b = benedict(d)
        b.swap("a.y", "b.y")
        b.swap("b.x", "c.x")
        r = {
            "a": {
                "x": 1,
                "y": 2,
            },
            "b": {
                "x": 3,
                "y": 1,
            },
            "c": {
                "x": 2,
                "y": 3,
            },
        }
        self.assertEqual(b, r)

        b.swap("a", "c")
        r = {
            "a": {
                "x": 2,
                "y": 3,
            },
            "b": {
                "x": 3,
                "y": 1,
            },
            "c": {
                "x": 1,
                "y": 2,
            },
        }
        self.assertEqual(b, r)

    def test_traverse(self):
        d = {
            "a": {
                "x": 2,
                "y": 3,
                "z": {
                    "ok": 5,
                },
            },
            "b": {
                "x": 7,
                "y": 11,
                "z": {
                    "ok": 13,
                },
            },
            "c": {
                "x": 17,
                "y": 19,
                "z": {
                    "ok": 23,
                },
            },
        }
        b = benedict(d)

        def f(parent, key, value):
            if not isinstance(value, dict):
                parent[key] = value + 1

        b.traverse(f)
        r = {
            "a": {
                "x": 3,
                "y": 4,
                "z": {
                    "ok": 6,
                },
            },
            "b": {
                "x": 8,
                "y": 12,
                "z": {
                    "ok": 14,
                },
            },
            "c": {
                "x": 18,
                "y": 20,
                "z": {
                    "ok": 24,
                },
            },
        }
        self.assertEqual(b, r)

    def test_unflatten(self):
        d = {
            "device_os": "Windows",
            "device_lang": "en-US",
            "device_code": 43,
            "browser_name": "Chrome",
            "browser_layout": "Webkit",
        }
        b = benedict(d)
        u = b.unflatten()
        r = {
            "device": {
                "os": "Windows",
                "lang": "en-US",
                "code": 43,
            },
            "browser": {
                "name": "Chrome",
                "layout": "Webkit",
            },
        }
        self.assertEqual(u, r)
        self.assertEqual(u.flatten(), b)
        self.assertEqual(type(b), type(u))
        self.assertTrue(isinstance(u, benedict))

    def test_unique(self):
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
                "x": 1,
                "y": 1,
            },
            "d": {
                "x": 1,
            },
            "e": {
                "x": 1,
                "y": 1,
                "z": 1,
            },
            "f": {
                "x": 2,
                "y": 2,
            },
        }
        b = benedict(d)
        b.unique()
        rv = [
            {
                "x": 1,
                "y": 1,
            },
            {
                "x": 2,
                "y": 2,
            },
            {
                "x": 1,
            },
            {
                "x": 1,
                "y": 1,
                "z": 1,
            },
        ]
        self.assertEqual(len(b.keys()), len(rv))
        self.assertTrue(all([value in rv for value in b.values()]))
