# -*- coding: utf-8 -*-

from benedict.dicts.base import BaseDict

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

import unittest


class base_dict_test_case(unittest.TestCase):

    def test__bool__(self):
        b = BaseDict()
        self.assertFalse(b)
        self.assertFalse(bool(b))
        self.assertEqual(b, b.dict())
        b = BaseDict()
        b['a'] = 1
        self.assertTrue(b)
        self.assertTrue(bool(b))
        self.assertEqual(b, b.dict())
        b = BaseDict({ 'a':1 })
        self.assertTrue(b)
        self.assertTrue(bool(b))
        self.assertEqual(b, b.dict())

    def test__contains__(self):
        b = BaseDict({ 'a':1 })
        self.assertTrue('a' in b)
        self.assertFalse('b' in b)
        self.assertEqual(b, b.dict())

    def test__delitem__(self):
        b = BaseDict({ 'a':1 })
        del b['a']
        self.assertFalse('a' in b)
        with self.assertRaises(KeyError):
            del b['b']
        self.assertEqual(b, b.dict())

    def test__equal__(self):
        b = BaseDict({ 'a':1 })
        o1 = { 'a':1 }
        o2 = { 'a':2 }
        self.assertTrue(b == o1)
        self.assertFalse(b == o2)
        self.assertEqual(b, b.dict())

    def test__getitem__(self):
        b = BaseDict({ 'a':1 })
        self.assertEqual(b['a'], 1)
        with self.assertRaises(KeyError):
            b['b']
        self.assertEqual(b, b.dict())

    def test__iter__(self):
        b = BaseDict({ 'a':1, 'b':2 })
        i = iter(b)
        self.assertTrue(isinstance(i, Iterable))
        self.assertEqual(b, b.dict())

    def test__len__(self):
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        self.assertEqual(len(b), 3)
        self.assertEqual(b, b.dict())

    def test__repr__(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        self.assertEqual(repr(d), repr(b))
        self.assertEqual(b, b.dict())

    def test__setitem__(self):
        b = BaseDict()
        b['a'] = 1
        self.assertEqual(b['a'], 1)
        self.assertEqual(b, b.dict())

    def test__str__(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        self.assertEqual(str(d), str(b))
        self.assertEqual(b, b.dict())

    def test_clear(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        b.clear()
        self.assertTrue(b == {})
        self.assertTrue(d == {})
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_copy(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        c = b.copy()
        c['a'] = -1
        c['b'] = -2
        c['c'] = -3
        self.assertTrue(b == d)
        self.assertFalse(b == c)
        # self.assertTrue(type(b) == type(c))
        self.assertEqual(b, b.dict())

    def test_dict(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        self.assertFalse(b is d)
        self.assertTrue(b.dict() is d)
        self.assertEqual(b, b.dict())

    def test_dict_pointer(self):
        d = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 3,
                'e': {
                    'f': 4,
                }
            }
        }
        b = BaseDict(d)
        b['a'] = -1
        b['b'] = -2
        b['c']['d'] = -3
        b['c']['e']['f'] = -4
        self.assertEqual(d, b)
        self.assertEqual(b, b.dict())

    def test_get(self):
        b = BaseDict({ 'a':1 })
        self.assertEqual(b.get('a'), 1)
        self.assertEqual(b.get('b'), None)
        self.assertEqual(b.get('b', 2), 2)
        self.assertEqual(b, b.dict())

    def test_items(self):
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        i = list(b.items())
        i.sort()
        self.assertTrue(i, [('a', 1, ), ('b', 2, ), ('c', 3, )])
        self.assertEqual(b, b.dict())

    def test_keys(self):
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        k = list(b.keys())
        k.sort()
        self.assertTrue(k, ['a', 'b', 'c'])
        self.assertEqual(b, b.dict())

    def test_pop(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        v = b.pop('c')
        self.assertEqual(v, 3)
        with self.assertRaises(KeyError):
            v = b.pop('d')
        v = b.pop('e', 5)
        self.assertEqual(v, 5)
        self.assertEqual(d, { 'a':1, 'b':2 })
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_setdefault(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        v = b.setdefault('c', 4)
        self.assertEqual(v, 3)
        v = b.setdefault('d', 4)
        self.assertEqual(v, 4)
        self.assertEqual(d, { 'a':1, 'b':2, 'c':3, 'd':4 })
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_update(self):
        d = { 'a':1, 'b':2, 'c':3 }
        b = BaseDict(d)
        b.update({ 'd':4, 'e':5 })
        self.assertEqual(d, { 'a':1, 'b':2, 'c':3, 'd':4, 'e':5 })
        self.assertTrue(b == d)
        self.assertEqual(b, b.dict())

    def test_values(self):
        b = BaseDict({ 'a':1, 'b':2, 'c':3 })
        v = list(b.values())
        v.sort()
        self.assertTrue(v, [1, 2, 3])
        self.assertEqual(b, b.dict())
