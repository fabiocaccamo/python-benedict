# -*- coding: utf-8 -*-

from benedict.utils import keylist_util

import unittest


class keylist_util_test_case(unittest.TestCase):

    def test_set_item_with_indexes(self):
        d = {}

        keylist_util.set_item(d, 'a', None)
        self.assertEqual(d, {'a':None})

        keylist_util.set_item(d, ['a', 'b', 'c'], 0)
        self.assertEqual(d, {'a':{'b':{'c':0}}})

        keylist_util.set_item(d, ['a', 'b', 'd'], 1)
        self.assertEqual(d, {'a':{'b':{'c':0,'d':1}}})
        # '[1]'
        keylist_util.set_item(d, ['a', 'b', 'e', 0], 1)
        keylist_util.set_item(d, ['a', 'b', 'e', 1], 2)
        keylist_util.set_item(d, ['a', 'b', 'e', 2], 3)
        self.assertEqual(d, { 'a':{ 'b':{ 'c':0, 'd':1, 'e':[1, 2, 3] }}})

        keylist_util.set_item(d, ['a', 'b', 'e', 0], 4)
        keylist_util.set_item(d, ['a', 'b', 'e', 1], 5)
        keylist_util.set_item(d, ['a', 'b', 'e', 2], 6)
        # keylist_util.set_item(d, ['a', 'b', 'e', 3], 7)
        # keylist_util.set_item(d, ['a', 'b', 'e', 4], 8)
        keylist_util.set_item(d, ['a', 'b', 'e', 5], 9)
        self.assertEqual(d, { 'a':{ 'b':{ 'c':0, 'd':1, 'e':[4, 5, 6, None, None, 9] }}})
        keylist_util.set_item(d, ['a', 'b', 'e', -11], 10)
        self.assertEqual(d, { 'a':{ 'b':{ 'c':0, 'd':1, 'e':[10, 4, 5, 6, None, None, 9] }}})

