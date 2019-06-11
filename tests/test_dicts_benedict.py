# -*- coding: utf-8 -*-

from benedict import benedict
from datetime import datetime
from decimal import Decimal

import unittest


class BenedictTestCase(unittest.TestCase):

    def test_copy(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        c = b.copy()
        self.assertEqual(type(b), type(c))
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c['a.b.c'] = 2
        self.assertEqual(b.get('a.b.c'), 2)
        self.assertEqual(c.get('a.b.c'), 2)

    def test_deepcopy(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        c = b.deepcopy()
        self.assertEqual(type(b), type(c))
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c['a.b.c'] = 2
        self.assertEqual(b.get('a.b.c'), 1)
        self.assertEqual(c.get('a.b.c'), 2)

    def test_dump(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        expected_output = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        output = benedict.dump(b)
        self.assertEqual(output, expected_output)

    def test_dump_items(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
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
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        expected_output = """{
    "c": 1
}"""
        output = b.dump_items('a.b')
        self.assertEqual(output, expected_output)

    def test_dump_items_with_datetime(self):
        d = {
            'datetime': datetime(2019, 6, 11),
        }
        b = benedict(d)
        expected_output = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        output = b.dump_items()
        self.assertEqual(output, expected_output)

    def test_dump_items_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        b = benedict(d)
        expected_output = """{
    "decimal": "1.75"
}"""
        output = b.dump_items()
        self.assertEqual(output, expected_output)

    def test_fromkeys(self):
        k = [
            'a',
            'a.b',
            'a.b.c',
            'a.b.d',
            'a.b.e',
            'x',
            'x.y',
            'x.z',
        ]
        b = benedict.fromkeys(k)
        r = {
            'x': {
                'y': None,
                'z': None,
            },
            'a': {
                'b': {
                    'c': None,
                    'd': None,
                    'e': None,
                },
            },
        }
        self.assertEqual(b, r)
        self.assertEqual(type(b), benedict)

    def test_fromkeys_with_value(self):
        k = [
            'a',
            'a.b',
            'a.b.c',
            'a.b.d',
            'a.b.e',
            'x',
            'x.y',
            'x.z',
        ]
        b = benedict.fromkeys(k, True)
        r = {
            'x': {
                'y': True,
                'z': True,
            },
            'a': {
                'b': {
                    'c': True,
                    'd': True,
                    'e': True,
                },
            },
        }
        self.assertEqual(b, r)
        self.assertEqual(type(b), benedict)

    def test_get_item(self):
        d = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3,
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b['a'], 1)
        self.assertEqual(b['b.c'], 2)
        self.assertTrue(isinstance(b['b'], benedict))
        self.assertTrue(isinstance(b['b.d'], benedict))
        bb = b['b']
        self.assertTrue(isinstance(bb['d'], benedict))

    def test_get_dict(self):
        d = {
            'a': {'x': 1, 'y': 2},
            'b': {},
        }
        b = benedict(d)
        self.assertTrue(isinstance(b.get_dict('a'), benedict))
        self.assertEqual(b.get('a.x'), 1)

    def test_get_list_item(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                }
            },
        }
        b = benedict(d)
        self.assertTrue(isinstance(b.get_dict('a'), benedict))
        self.assertTrue(isinstance(b.get_dict('a.b'), benedict))
        self.assertEqual(b.get('a.b.c'), 1)

    def test_get(self):
        d = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3,
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b.get('a'), 1)
        self.assertEqual(b.get('b.c'), 2)
        self.assertTrue(isinstance(b.get('b'), benedict))
        self.assertTrue(isinstance(b.get('b.d'), benedict))
        bb = b.get('b')
        self.assertTrue(isinstance(bb.get('d'), benedict))

    def test_pop(self):
        d = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3,
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b.pop('a'), 1)
        self.assertEqual(b.pop('b.c'), 2)
        self.assertTrue(isinstance(b.pop('b.d'), benedict))

    def test_setdefault(self):
        d = {
            'a': 1,
            'b': {
                'c': 2,
                'd': {
                    'e': 3,
                }
            }
        }
        b = benedict(d)
        self.assertTrue(isinstance(b.setdefault('b', 1), benedict))
        self.assertTrue(isinstance(b.setdefault('b.d', 1), benedict))
