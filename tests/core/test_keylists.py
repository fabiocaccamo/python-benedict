# -*- coding: utf-8 -*-

from benedict.core import keylists as _keylists

import unittest


class keylists_test_case(unittest.TestCase):

    def test_keylists(self):
        i = {
            'a': 1,
            'b': {
                'c': {
                    'x': 2,
                    'y': 3,
                },
                'd': {
                    'x': 4,
                    'y': 5,
                },
            },
        }
        o = _keylists(i)
        r = [
            ['a'],
            ['b'],
            ['b', 'c'],
            ['b', 'c', 'x'],
            ['b', 'c', 'y'],
            ['b', 'd'],
            ['b', 'd', 'x'],
            ['b', 'd', 'y'],
        ]
        self.assertEqual(o, r)

    def test_keylists_with_non_string_keys(self):
        i = {
            True: {
                True: 1,
            },
            False: {
                False: 1,
            },
            None: {
                None: 1,
            },
        }
        o = _keylists(i)
        r = [
            [False],
            [False, False],
            [None],
            [None, None],
            [True],
            [True, True],
        ]
        for k in r:
            self.assertTrue(k in o)
