# -*- coding: utf-8 -*-

from benedict.core import invert as _invert

import unittest


class invert_test_case(unittest.TestCase):

    def test_invert_with_unique_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        o = _invert(i)
        r = {
            1: ['a'],
            2: ['b'],
            3: ['c'],
            4: ['d'],
            5: ['e'],
        }
        self.assertEqual(o, r)

    def test_invert_with_flat_unique_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        o = _invert(i, flat=True)
        r = {
            1: 'a',
            2: 'b',
            3: 'c',
            4: 'd',
            5: 'e',
        }
        self.assertEqual(o, r)

    def test_invert_with_multiple_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 1,
            'e': 2,
            'f': 3,
        }
        o = _invert(i)
        self.assertTrue('a' and 'd' in o[1])
        self.assertTrue('b' and 'e' in o[2])
        self.assertTrue('c' and 'f' in o[3])

    def test_invert_with_list_values(self):
        i = {
            'a': ['x', 'y', 'z'],
            'b': ['c', 'd', 'e'],
        }
        o = _invert(i)
        r = {
            'x': ['a'],
            'y': ['a'],
            'z': ['a'],
            'c': ['b'],
            'd': ['b'],
            'e': ['b'],
        }
        self.assertEqual(o, r)
        self.assertEqual(_invert(o), i)

    def test_invert_with_tuple_values(self):
        i = {
            'a': ('x', 'y', 'z', ),
            'b': ('c', 'd', 'e', ),
        }
        o = _invert(i)
        r = {
            'x': ['a', ],
            'y': ['a', ],
            'z': ['a', ],
            'c': ['b', ],
            'd': ['b', ],
            'e': ['b', ],
        }
        self.assertEqual(o, r)
