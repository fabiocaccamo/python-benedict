import copy
import sys
import unittest
from collections.abc import Iterable

from benedict.dicts.base import BaseDict


class base_dict_test_case(unittest.TestCase):
    """
    This class describes a BaseDict test case.
    """

    def test__bool__(self):
        b = BaseDict()
        self.assertFalse(b)
        self.assertFalse(bool(b))
        self.assertEqual(b, b.dict())
        b = BaseDict()
        b["a"] = 1
        self.assertTrue(b)
        self.assertTrue(bool(b))
        self.assertEqual(b, b.dict())

    def test__bool__with_pointer(self):
        d = {"a": 1}
        b = BaseDict(d)
        self.assertTrue(b)
        self.assertTrue(bool(b))
        self.assertEqual(b, b.dict())
        b = BaseDict({})
        self.assertFalse(b)
        self.assertFalse(bool(b))
        self.assertEqual(b, b.dict())

    def test__contains__(self):
        b = BaseDict()
        b["a"] = 1
        self.assertTrue("a" in b)
        self.assertFalse("b" in b)
        self.assertEqual(b, b.dict())

    def test__contains__with_pointer(self):
        d = {"a": 1}
        b = BaseDict(d)
        self.assertTrue("a" in b)
        self.assertFalse("b" in b)
        self.assertEqual(b, b.dict())
        del d["a"]
        self.assertFalse("a" in b)

    def test__deepcopy__(self):
        b1 = BaseDict()
        b1["a"] = {}
        b1["a"]["b"] = {}
        b1["a"]["b"]["c"] = True
        b2 = copy.deepcopy(b1)
        self.assertEqual(b1, b2)
        self.assertEqual(type(b1), type(b2))
        self.assertFalse(b1 is b2)

    def test__deepcopy__with_pointer(self):
        d = {}
        d["a"] = {}
        d["a"]["b"] = {}
        d["a"]["b"]["c"] = True
        b1 = BaseDict(d)
        b2 = copy.deepcopy(b1)
        self.assertEqual(b1, b2)
        self.assertEqual(type(b1), type(b2))
        self.assertFalse(b1 is b2)

    def test__delitem__(self):
        b = BaseDict()
        with self.assertRaises(KeyError):
            del b["a"]
        self.assertEqual(b, b.dict())

    def test__delitem__with_pointer(self):
        d = {
            "a": 1,
        }
        b = BaseDict(d)
        self.assertTrue("a" in b)
        del b["a"]
        self.assertFalse("a" in b)
        with self.assertRaises(KeyError):
            del b["a"]
        self.assertEqual(b, b.dict())

    def test__equal__(self):
        b = BaseDict()
        o1 = {}
        o2 = {
            "a": 2,
        }
        self.assertTrue(b == o1)
        self.assertFalse(b == o2)
        self.assertEqual(b, b.dict())

    def test__equal__with_pointer(self):
        d = {
            "a": 1,
        }
        b = BaseDict(d)
        o1 = {
            "a": 1,
        }
        o2 = {
            "a": 2,
        }
        self.assertTrue(b == o1)
        self.assertFalse(b == o2)
        self.assertEqual(b, b.dict())

    def test__getitem__(self):
        b = BaseDict()
        with self.assertRaises(KeyError):
            b["a"]
        self.assertEqual(b, b.dict())

    def test__getitem__with_pointer(self):
        d = {
            "a": 1,
        }
        b = BaseDict(d)
        self.assertEqual(b["a"], 1)
        self.assertEqual(b, b.dict())

    def test__iter__(self):
        b = BaseDict()
        i = iter(b)
        self.assertTrue(isinstance(i, Iterable))
        self.assertEqual(b, b.dict())

    def test__iter__with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
        }
        b = BaseDict(d)
        i = iter(b)
        self.assertTrue(isinstance(i, Iterable))
        self.assertEqual(b, b.dict())

    def test__len__(self):
        b = BaseDict()
        self.assertEqual(len(b), 0)
        b["a"] = 1
        self.assertEqual(len(b), 1)
        self.assertEqual(b, b.dict())

    def test__len__with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        self.assertEqual(len(b), 3)
        self.assertEqual(len(d), 3)
        b["d"] = 4
        self.assertEqual(len(b), 4)
        self.assertEqual(len(d), 4)
        self.assertEqual(b, b.dict())

    def test__repr__(self):
        d = {}
        b = BaseDict()
        self.assertEqual(repr(d), repr(b))
        self.assertEqual(b, b.dict())

    def test__repr__with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        self.assertEqual(repr(d), repr(b))
        self.assertEqual(b, b.dict())

    def test__setitem__(self):
        b = BaseDict()
        b["a"] = 1
        self.assertEqual(b["a"], 1)
        self.assertEqual(b, b.dict())

    def test__setitem__with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        b["a"] = 2
        self.assertEqual(b["a"], 2)
        self.assertEqual(d["a"], 2)
        self.assertEqual(b, b.dict())

    def test__str__(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(
            {
                "a": 1,
                "b": 2,
                "c": 3,
            }
        )
        self.assertEqual(str(d), str(b))
        self.assertEqual(b, b.dict())

    def test__str__with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        self.assertEqual(str(d), str(b))
        self.assertEqual(b, b.dict())

    @unittest.skipIf(sys.version_info[0] > 2, "No unicode in Python 3")
    def test__unicode__(self):
        d = BaseDict()
        d["name"] = "pythòn-bènèdìçt"
        # print(unicode(d))

    @unittest.skipIf(sys.version_info[0] > 2, "No unicode in Python > 2")
    def test__unicode__with_pointer(self):
        d = BaseDict({"name": "pythòn-bènèdìçt"})
        # print(unicode(d))

    def test_clear(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        self.assertTrue(b == d)
        b.clear()
        self.assertTrue(b == {})
        self.assertTrue(d != {})

    def test_clear_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        b.clear()
        self.assertTrue(b == {})
        self.assertTrue(d == {})
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_copy(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        c = b.copy()
        c["a"] = -1
        c["b"] = -2
        c["c"] = -3
        self.assertFalse(b == c)
        # self.assertTrue(type(b) == type(c))
        self.assertEqual(b, b.dict())

    def test_copy_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        c = b.copy()
        c["a"] = -1
        c["b"] = -2
        c["c"] = -3
        self.assertTrue(b == d)
        self.assertFalse(b == c)
        # self.assertTrue(type(b) == type(c))
        self.assertEqual(b, b.dict())

    def test_dict(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        self.assertFalse(b is d)
        self.assertTrue(b.dict() is d)
        self.assertEqual(b, b.dict())

    def test_dict_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": {
                "d": 3,
                "e": {
                    "f": 4,
                },
            },
        }
        b = BaseDict(d)
        b["a"] = -1
        b["b"] = -2
        b["c"]["d"] = -3
        b["c"]["e"]["f"] = -4
        self.assertEqual(d, b)
        self.assertEqual(b, b.dict())

    def test_get(self):
        b = BaseDict()
        b["a"] = 1
        self.assertEqual(b.get("a"), 1)
        self.assertEqual(b.get("b"), None)
        self.assertEqual(b.get("b", 2), 2)
        self.assertEqual(b, b.dict())

    def test_get_with_pointer(self):
        d = {
            "a": 1,
        }
        b = BaseDict(d)
        self.assertEqual(b.get("a"), 1)
        d["a"] = 2
        self.assertEqual(b.get("a"), 2)
        self.assertEqual(b.get("b"), None)
        self.assertEqual(b.get("b", 2), 2)
        self.assertEqual(b, b.dict())

    def test_items(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        i = list(b.items())
        i.sort()
        self.assertTrue(i, [("a", 1), ("b", 2), ("c", 3)])
        self.assertEqual(b, b.dict())

    def test_items_with_pointer(self):
        d = {"a": 1, "b": 2, "c": 3}
        b = BaseDict(d)
        i = list(b.items())
        i.sort()
        self.assertTrue(i, [("a", 1), ("b", 2), ("c", 3)])
        self.assertEqual(b, b.dict())

    def test_keys(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        k = list(b.keys())
        k.sort()
        self.assertTrue(k, ["a", "b", "c"])
        self.assertEqual(b, b.dict())

    def test_keys_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        k = list(b.keys())
        k.sort()
        self.assertTrue(k, ["a", "b", "c"])
        self.assertEqual(b, b.dict())

    def test_pop(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        v = b.pop("c")
        self.assertEqual(v, 3)
        with self.assertRaises(KeyError):
            v = b.pop("d")
        v = b.pop("e", 5)
        self.assertEqual(v, 5)
        self.assertEqual(b, b.dict())

    def test_pop_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        v = b.pop("c")
        self.assertEqual(v, 3)
        with self.assertRaises(KeyError):
            v = b.pop("d")
        v = b.pop("e", 5)
        self.assertEqual(v, 5)
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
            },
        )
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_setdefault(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        v = b.setdefault("c", 4)
        self.assertEqual(v, 3)
        v = b.setdefault("d", 4)
        self.assertEqual(v, 4)
        self.assertEqual(b, b.dict())

    def test_setdefault_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        v = b.setdefault("c", 4)
        self.assertEqual(v, 3)
        v = b.setdefault("d", 4)
        self.assertEqual(v, 4)
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
            },
        )
        d["d"] = 4
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_update(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        b.update(
            {
                "d": 4,
                "e": 5,
            }
        )
        self.assertEqual(b, {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})
        self.assertEqual(b, b.dict())

    def test_update_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        b.update(
            {
                "d": 4,
                "e": 5,
            }
        )
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": 2,
                "c": 3,
                "d": 4,
                "e": 5,
            },
        )
        d["a"] = -1
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_values(self):
        b = BaseDict()
        b["a"] = 1
        b["b"] = 2
        b["c"] = 3
        v = list(b.values())
        v.sort()
        self.assertTrue(v, [1, 2, 3])
        self.assertEqual(b, b.dict())

    def test_values_with_pointer(self):
        d = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        b = BaseDict(d)
        v = list(b.values())
        v.sort()
        self.assertTrue(v, [1, 2, 3])
        self.assertEqual(b, b.dict())
