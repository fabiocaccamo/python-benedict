import unittest

from benedict import benedict


class benedict_casting_test_case(unittest.TestCase):
    """
    This class describes a benedict casting test case.
    """

    def test__getitem__(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        c = b["b.c"]
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(type(c), benedict)
        self.assertTrue(c == d["b"]["c"])
        self.assertFalse(c is d["b"]["c"])

    def test_cast_dict_to_benedict(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        bb = benedict(b)
        bbd = bb.dict()
        self.assertTrue(isinstance(bbd, dict))
        self.assertFalse(isinstance(bbd, benedict))
        self.assertEqual(d, bbd)
        self.assertTrue(d is bbd)

    def test_cast_benedict_to_dict(self):
        b = benedict(
            {
                "a": 1,
                "b": {
                    "c": {
                        "d": 2,
                    },
                },
            }
        )
        # d1 = dict(**b)
        # print(d1)
        d = dict(b)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(type(d), dict)
        self.assertEqual(b, d)
        self.assertFalse(b is d)
        d = dict(b)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(type(d), dict)
        self.assertEqual(b, d)
        self.assertFalse(b is d)

    def test_cast_benedict_kwargs_to_dict(self):
        b = benedict(
            {
                "a": 1,
                "b": {
                    "c": {
                        "d": 2,
                    },
                },
            }
        )
        d = dict(**b)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(type(d), dict)
        self.assertEqual(b, d)
        self.assertFalse(b is d)

    def test_dict(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        bd = b.dict()
        self.assertTrue(isinstance(bd, dict))
        self.assertFalse(isinstance(bd, benedict))
        self.assertTrue(d == bd)
        self.assertTrue(d is bd)

    def test_get(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        c = b.get("b.c")
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(type(c), benedict)
        self.assertTrue(c == d["b"]["c"])
        self.assertFalse(c is d["b"]["c"])

    def test_get_dict(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        c = b.get_dict("b.c")
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(type(c), benedict)
        self.assertTrue(c == d["b"]["c"])
        self.assertFalse(c is d["b"]["c"])

    def test_get_list_item(self):
        d = {
            "a": 1,
            "b": {
                "c": [
                    {
                        "d": 2,
                    },
                    {
                        "e": 3,
                    },
                    {
                        "f": 4,
                    },
                ]
            },
        }
        b = benedict(d)
        c = b.get_list_item("b.c", 1)
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(type(c), benedict)
        self.assertTrue(c == d["b"]["c"][1])
        self.assertFalse(c is d["b"]["c"][1])

    def test_pop(self):
        d = {
            "a": 1,
            "b": {
                "c": {
                    "d": 2,
                },
            },
        }
        b = benedict(d)
        c = b.pop("b.c")
        self.assertTrue(isinstance(c, benedict))
        self.assertEqual(type(c), benedict)
        with self.assertRaises(KeyError):
            d["b"]["c"]
