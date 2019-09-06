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

    def test_clone(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = UtilityDict(d)
        c = b.clone()
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c['a']['b']['c'] = 2
        self.assertEqual(b['a']['b']['c'], 1)
        self.assertEqual(c['a']['b']['c'], 2)

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

    def test_deepupdate_with_single_dict(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
        }
        d = UtilityDict(d)
        d.deepupdate(a)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        self.assertEqual(d, r)

    def test_deepupdate_with_multiple_dicts(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
            'd': 3,
        }
        b = {
            'd': 5,
            'e': 5,
        }
        c = {
            'd': 4,
            'f': 6,
        }
        d = UtilityDict(d)
        d.deepupdate(a, b, c)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        self.assertEqual(d, r)

    def test_deepupdate(self):
        d = {
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
                'e': {
                    'x': 6,
                    'y': 7,
                },
            },
        }
        a = {
            'a': 0,
            'b': {
                'c': 1,
                'd': {
                    'y': 1,
                    'z': 2,
                },
                'e': {
                    'f': {
                        'x': 2,
                        'y': 3,
                    },
                    'g': {
                        'x': 4,
                        'y': 5,
                    },
                },
            },
        }
        d = UtilityDict(d)
        d.deepupdate(a)
        r = {
            'a': 0,
            'b': {
                'c': 1,
                'd': {
                    'x': 4,
                    'y': 1,
                    'z': 2,
                },
                'e': {
                    'f': {
                        'x': 2,
                        'y': 3,
                    },
                    'g': {
                        'x': 4,
                        'y': 5,
                    },
                    'x': 6,
                    'y': 7,
                },
            },
        }
        self.assertEqual(d, r)

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
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_datetime(self):
        d = {
            'datetime': datetime(2019, 6, 11),
        }
        b = UtilityDict(d)
        expected_output = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        b = UtilityDict(d)
        expected_output = """{
    "decimal": "1.75"
}"""
        output = b.dump()
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

    def test_merge_with_single_dict(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
        }
        d = UtilityDict(d)
        d.merge(a)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        self.assertEqual(d, r)

    def test_merge_with_multiple_dicts(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
            'd': 3,
        }
        b = {
            'd': 5,
            'e': 5,
        }
        c = {
            'd': 4,
            'f': 6,
        }
        d = UtilityDict(d)
        d.merge(a, b, c)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        self.assertEqual(d, r)

    def test_merge(self):
        d = {
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
                'e': {
                    'x': 6,
                    'y': 7,
                },
            },
        }
        a = {
            'a': 0,
            'b': {
                'c': 1,
                'd': {
                    'y': 1,
                    'z': 2,
                },
                'e': {
                    'f': {
                        'x': 2,
                        'y': 3,
                    },
                    'g': {
                        'x': 4,
                        'y': 5,
                    },
                },
            },
        }
        d = UtilityDict(d)
        d.merge(a)
        r = {
            'a': 0,
            'b': {
                'c': 1,
                'd': {
                    'x': 4,
                    'y': 1,
                    'z': 2,
                },
                'e': {
                    'f': {
                        'x': 2,
                        'y': 3,
                    },
                    'g': {
                        'x': 4,
                        'y': 5,
                    },
                    'x': 6,
                    'y': 7,
                },
            },
        }
        self.assertEqual(d, r)

    def test_remove(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = UtilityDict(d)
        b.remove(['c', 'e', 'f', 'g'])
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(b, r)

    def test_subset(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = UtilityDict(d)
        f = b.subset(['c', 'f', 'x'])
        r = {
            'c': '4',
            'f': 6,
            'x': None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
