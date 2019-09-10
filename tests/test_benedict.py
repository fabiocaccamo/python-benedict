# -*- coding: utf-8 -*-

from benedict import benedict
from datetime import datetime
from decimal import Decimal

import unittest


class BenedictTestCase(unittest.TestCase):

    def test_cast(self):
        d = {
            'a': 1,
        }
        b = benedict.cast(d)
        self.assertEqual(d, b)
        self.assertFalse(b is d)
        self.assertTrue(isinstance(b, benedict))
        v = [0, 1, 2, 3]
        b = benedict.cast(v)
        self.assertEqual(v, b)
        self.assertTrue(b is v)
        self.assertFalse(isinstance(b, benedict))

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
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_datetime(self):
        d = {
            'datetime': datetime(2019, 6, 11),
        }
        b = benedict(d)
        expected_output = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_dump_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        b = benedict(d)
        expected_output = """{
    "decimal": "1.75"
}"""
        output = b.dump()
        self.assertEqual(output, expected_output)

    def test_filter(self):
        d = {
            'a': {
                'ok': 'yes',
            },
            'b': {
                'ok': 'no',
            },
            'c': {
                'ok': 'yes',
            },
            'e': {
                'ok': 'no',
            },
            'f': {
                'ok': 'yes',
            },
            'g': {
                'ok': 'no',
            },
        }
        b = benedict(d)
        f = b.filter(lambda key, val: val.get_bool('ok'))
        r = {
            'a': {
                'ok': 'yes',
            },
            'c': {
                'ok': 'yes',
            },
            'f': {
                'ok': 'yes',
            },
        }
        self.assertEqual(f, r)
        self.assertTrue(isinstance(f, benedict))

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

    def test_from_json(self):
        j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = benedict.from_json(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor
        d = benedict(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

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

    def test_get_list(self):
        d = {
            'a': [
                {
                    'b': {
                        'c': 1,
                    }
                },
                {
                    'b': {
                        'c': 2,
                    }
                },
                {
                    'b': {
                        'c': 3,
                    }
                },
            ]
        }
        b = benedict(d)
        l = b.get_list('a')
        self.assertTrue(isinstance(l[0], benedict))
        self.assertTrue(isinstance(l[1], benedict))
        self.assertTrue(isinstance(l[2], benedict))
        self.assertEqual(l[0].get('b.c'), 1)
        self.assertEqual(l[1].get('b.c'), 2)
        self.assertEqual(l[2].get('b.c'), 3)

    def test_get_list_item(self):
        d = {
            'a': [
                {
                    'b': {
                        'c': 1,
                    }
                },
                {
                    'b': {
                        'c': 2,
                    }
                },
                {
                    'b': {
                        'c': 3,
                    }
                },
            ]
        }
        b = benedict(d)
        i = b.get_list_item('a', index=1)
        self.assertTrue(isinstance(i, benedict))
        self.assertEqual(i.get('b.c'), 2)

    def test_get_phonenumber(self):
        d = {
            'a': {
                'b': ' (0039) 3334445566 ',
                'c': '+393334445566  ',
                'd': '+39333444556677889900',
            }
        }
        r = {
            'e164': '+393334445566',
            'international': '+39 333 444 5566',
            'national': '333 444 5566'
        }
        b = benedict(d)

        p = b.get_phonenumber('a.b')
        self.assertEqual(p, r)
        self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber('a.c')
        self.assertEqual(p, r)
        self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber('a.d')
        self.assertEqual(p, {})
        self.assertTrue(isinstance(p, benedict))

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

    def test_remove(self):
        d = {
            'a': {
                'x': 1,
                'y': 1,
            },
            'b': {
                'x': 2,
                'y': 2,
            },
            'c': {
                'x': 3,
                'y': 3,
            },
            'd': {
                'x': 4,
                'y': 4,
            },
        }
        b = benedict(d)
        b.remove(['a.x', 'b.y', 'c.x', 'c.y', 'd'])
        r = {
            'a': {
                'y': 1
            },
            'b': {
                'x': 2
            },
            'c': {
            },
        }
        self.assertEqual(b, r)

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

    def test_subset(self):
        d = {
            'x': {
                'a': 1,
                'aa': 1,
            },
            'y': {
                'b': 2,
                'bb': 2,
            },
            'z': {
                'c': 3,
                'cc': 3,
            },
        }
        b = benedict(d)
        f = b.subset(['x', 'y'])
        r = {
            'x': {
                'a': 1,
                'aa': 1,
            },
            'y': {
                'b': 2,
                'bb': 2,
            },
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f.get('x.a'), 1)
        self.assertEqual(f.get('x.aa'), 1)
        self.assertEqual(f.get('y.b'), 2)
        self.assertEqual(f.get('y.bb'), 2)
        # test with keypath
        f = b.subset(['x.a', 'y.b'])
        r = {
            'x': {
                'a': 1,
            },
            'y': {
                'b': 2,
            },
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)
        self.assertTrue(isinstance(f, benedict))
        self.assertEqual(f.get('x.a'), 1)
        self.assertEqual(f.get('y.b'), 2)
