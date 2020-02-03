# -*- coding: utf-8 -*-

from benedict.core import keypaths as _keypaths

import unittest


class keypaths_test_case(unittest.TestCase):

    def test_keypaths(self):
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
        o = _keypaths(i)
        r = [
            'a',
            'b',
            'b.c',
            'b.c.x',
            'b.c.y',
            'b.d',
            'b.d.x',
            'b.d.y',
        ]
        self.assertEqual(o, r)

    def test_keypaths_with_custom_separator(self):
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
        o = _keypaths(i, separator='/')
        r = [
            'a',
            'b',
            'b/c',
            'b/c/x',
            'b/c/y',
            'b/d',
            'b/d/x',
            'b/d/y',
        ]
        self.assertEqual(o, r)

    def test_keypaths_without_separator(self):
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
        with self.assertRaises(ValueError):
            o = _keypaths(i, separator=None)

    def test_keypaths_with_non_string_keys(self):
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
        o = _keypaths(i)
        r = [
            'False',
            'False.False',
            'None',
            'None.None',
            'True',
            'True.True',
        ]
        self.assertEqual(o, r)
