# -*- coding: utf-8 -*-

from benedict.dicts import UtilityDict
from datetime import datetime
from decimal import Decimal

import unittest


class UtilityDictTestCase(unittest.TestCase):

    def test_clean(self):
        d = {
            'a': {},
            'b': { 'x': 1 },
            'c': [],
            'd': [0, 1],
            'e': 0.0,
            'f': '',
            'g': None,
            'h': '0'
        }

        b = UtilityDict(d)
        b.clean()
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'h': '0',
        }
        self.assertEqual(b, r)

        b = UtilityDict(d)
        b.clean(dicts=False)
        r = {
            'a': {},
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'h': '0'
        }
        self.assertEqual(b, r)

        b = UtilityDict(d)
        b.clean(lists=False)
        r = {
            'b': { 'x': 1 },
            'c': [],
            'd': [0, 1],
            'e': 0.0,
            'h': '0'
        }
        self.assertEqual(b, r)

        b = UtilityDict(d)
        b.clean(strings=False)
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'f': '',
            'h': '0',
        }
        self.assertEqual(b, r)

    def test_deepcopy(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = UtilityDict(d)
        c = b.deepcopy()
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c['a']['b']['c'] = 2
        self.assertEqual(b['a']['b']['c'], 1)
        self.assertEqual(c['a']['b']['c'], 2)

    def test_dump(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = UtilityDict(d)
        expected_output = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        output = UtilityDict.dump(b)
        self.assertEqual(output, expected_output)

    def test_dump_items(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = UtilityDict(d)
        print(b.dump_items())
        expected_output = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        output = b.dump_items()
        self.assertEqual(output, expected_output)

    def test_dump_items_with_key(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = UtilityDict(d)
        expected_output = """{
    "b": 1
}"""
        output = b.dump_items('a')
        self.assertEqual(output, expected_output)

    def test_dump_items_with_datetime(self):
        d = {
            'datetime': datetime(2019, 6, 11),
        }
        b = UtilityDict(d)
        expected_output = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        output = b.dump_items()
        self.assertEqual(output, expected_output)

    def test_dump_items_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        b = UtilityDict(d)
        expected_output = """{
    "decimal": "1.75"
}"""
        output = b.dump_items()
        self.assertEqual(output, expected_output)

    def test_filter(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = UtilityDict(d)
        with self.assertRaises(ValueError):
            f = b.filter(True)
        f = b.filter(lambda key, val: isinstance(val, int))
        r = {
            'a': 1,
            'b': 2,
            'f': 6,
            'g': 7,
        }
        self.assertEqual(f, r)
        self.assertFalse(b is f)

