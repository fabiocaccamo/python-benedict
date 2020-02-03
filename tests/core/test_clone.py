# -*- coding: utf-8 -*-

from benedict.core import clone as _clone

import unittest


class clone_test_case(unittest.TestCase):

    def test_clone(self):
        i = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        o = _clone(i)
        self.assertEqual(type(i), type(o))
        self.assertEqual(i, o)
        self.assertFalse(i is o)
        o['a']['b']['c'] = 2
        self.assertEqual(i['a']['b']['c'], 1)
        self.assertEqual(o['a']['b']['c'], 2)
