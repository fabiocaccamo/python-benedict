# -*- coding: utf-8 -*-

from benedict.utils import keylist_util, keypath_util

import unittest


class keypath_util_test_case(unittest.TestCase):

    def test_split_key_indexes_with_valid_indexes(self):
        f = keypath_util._split_key_indexes
        self.assertEqual(f('item[0]'), ['item', 0])
        self.assertEqual(f('item[1]'), ['item', 1])
        self.assertEqual(f('item[-1]'), ['item', -1])
        self.assertEqual(f('item[10]'), ['item', 10])
        self.assertEqual(f('item[0][0]'), ['item', 0, 0])
        self.assertEqual(f('item[0][1]'), ['item', 0, 1])
        self.assertEqual(f('item[1][1]'), ['item', 1, 1])
        self.assertEqual(f('item[-1][-1]'), ['item', -1, -1])
        self.assertEqual(f('item[10][10]'), ['item', 10, 10])
        self.assertEqual(f("item['0']['-1']"), ['item', 0, -1])
        self.assertEqual(f('item[\'0\'][\'-1\']'), ['item', 0, -1])
        self.assertEqual(f('item["0"]["-1"]'), ['item', 0, -1])
        self.assertEqual(f("item[\"0\"][\"-1\"]"), ['item', 0, -1])

    def test_split_key_indexes_with_invalid_indexes(self):
        f = keypath_util._split_key_indexes
        self.assertEqual(f('item[]'), ['item[]'])
        self.assertEqual(f('item[*]'), ['item[*]'])
        self.assertEqual(f('item[0:2]'), ['item[0:2]'])
        self.assertEqual(f('item[:1]'), ['item[:1]'])
        self.assertEqual(f('item[::1]'), ['item[::1]'])
        self.assertEqual(f('item[--1]'), ['item[--1]'])
        self.assertEqual(f('item[-1]1'), ['item[-1]1'])
        self.assertEqual(f('item[-1]1]'), ['item[-1]1]'])
        self.assertEqual(f('item[-1]]'), ['item[-1]]'])
        self.assertEqual(f('item[[-1]]'), ['item[[-1]]'])
        self.assertEqual(f('item[0:2][0:2]'), ['item[0:2][0:2]'])
        self.assertEqual(f('item[:1][:1]'), ['item[:1][:1]'])
        self.assertEqual(f('item[::1][::1]'), ['item[::1][::1]'])
        self.assertEqual(f('item[--1][--1]'), ['item[--1][--1]'])
        self.assertEqual(f('item[-1]1[-1]1'), ['item[-1]1[-1]1'])
        self.assertEqual(f('item[-1]1][-1]1]'), ['item[-1]1][-1]1]'])
        self.assertEqual(f('item[-1]][-1]]'), ['item[-1]][-1]]'])
        self.assertEqual(f('item[[-1]][[-1]]'), ['item[[-1]][[-1]]'])
