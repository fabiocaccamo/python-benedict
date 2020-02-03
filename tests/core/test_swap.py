# -*- coding: utf-8 -*-

from benedict.core import swap as _swap

import unittest


class swap_test_case(unittest.TestCase):

    def test_swap(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        _swap(d, 'a', 'b')
        r = {
            'a': 2,
            'b': 1,
            'c': 3,
        }
        self.assertEqual(d, r)

    def test_swap_with_same_key(self):
        d = {
            'a': 1,
            'b': 2,
        }
        _swap(d, 'a', 'a')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(d, r)

    def test_swap_with_invalid_key(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        with self.assertRaises(KeyError):
            _swap(d, 'a', 'd')
