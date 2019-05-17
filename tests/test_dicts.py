# -*- coding: utf-8 -*-

from benedict import benedict
from datetime import datetime
from decimal import Decimal

import unittest


class BenedictKeypathDictTestCase(unittest.TestCase):

    def test_get_with_1_valid_key(self):
        d = {
            'a': 1,
            1: 1
        }
        b = benedict(d)
        self.assertEqual(b.get('a', 2), 1)
        self.assertEqual(b.get(1, 2), 1)

    def test_get_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = benedict(d)
        self.assertEqual(b.get('b', 2), 2)

    def test_get_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
            0: 0,
        }
        b = benedict(d)
        self.assertEqual(b.get(None, 1), None)
        self.assertEqual(b.get(False, True), False)
        self.assertEqual(b.get(True, True), True)
        self.assertEqual(b.get(0, 1), 0)

    def test_getitem_with_1_valid_key(self):
        d = {
            'a': 1,
        }
        b = benedict(d)
        self.assertEqual(b['a'], 1)

    def test_getitem_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = benedict(d)
        self.assertEqual(b['b'], None)

    def test_getitem_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
            0: 0,
        }
        b = benedict(d)
        self.assertEqual(b[None], None)
        self.assertEqual(b[False], False)
        self.assertEqual(b[True], None)
        self.assertEqual(b[0], 0)

    def test_get_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = benedict(d)
        self.assertEqual(b.get('a.b', 2), 1)

    def test_get_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = benedict(d)
        self.assertEqual(b.get('b.a', 2), 2)

    def test_getitem_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = benedict(d)
        self.assertEqual(b['a.b'], 1)

    def test_getitem_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = benedict(d)
        self.assertEqual(b['b.a'], None)

    def test_get_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b.get('a.b.c', 2), 1)

    def test_get_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b.get('c.b.a', 2), 2)

    def test_getitem_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b['a.b.c'], 1)

    def test_getitem_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        self.assertEqual(b['c.b.a'], None)

    def test_has_with_1_key(self):
        d = {
            'a': 0,
            'b': None,
            'c': {},
        }
        b = benedict(d)
        self.assertTrue('a' in b)
        self.assertTrue('b' in b)
        self.assertTrue('c' in b)
        self.assertFalse('d' in b)

    def test_has_with_2_keys(self):
        d = {
            'a': {
                'a': 0,
                'b': None,
                'c': {},
            },
        }
        b = benedict(d)
        self.assertTrue('a.a' in b)
        self.assertTrue('a.b' in b)
        self.assertTrue('a.c' in b)
        self.assertFalse('a.d' in b)
        self.assertFalse('b' in b)
        self.assertFalse('b.a' in b)

    def test_has_with_3_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 0,
                    'd': None,
                    'e': {},
                },
            },
        }
        b = benedict(d)
        self.assertTrue('a.b.c' in b)
        self.assertTrue('a.b.d' in b)
        self.assertTrue('a.b.e' in b)
        self.assertFalse('a.b.f' in b)
        self.assertFalse('b.f' in b)
        self.assertFalse('f' in b)

    def test_set_override_existing_item(self):
        d = {}
        b = benedict(d)
        b.set('a.b.c', 1)
        r = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b.set('a.b.c', 2)
        r = {
            'a': {
                'b': {
                    'c': 2
                }
            }
        }
        self.assertEqual(b, r)
        b.set('a.b.c.d', 3)
        r = {
            'a': {
                'b': {
                    'c': {
                        'd': 3
                    }
                }
            }
        }
        self.assertEqual(b, r)

    def test_setitem_override_existing_item(self):
        d = {}
        b = benedict(d)
        b['a.b.c'] = 1
        r = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b['a.b.c'] = 2
        r = {
            'a': {
                'b': {
                    'c': 2
                }
            }
        }
        self.assertEqual(b, r)
        b['a.b.c.d'] = 3
        r = {
            'a': {
                'b': {
                    'c': {
                        'd': 3
                    }
                }
            }
        }
        self.assertEqual(b, r)

    def test_delitem_with_1_valid_key(self):
        d = {
            'a': 1,
        }
        b = benedict(d)
        del b['a']
        self.assertEqual(b['a'], None)

    def test_delitem_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = benedict(d)
        del b['b']
        self.assertEqual(b['a'], 1)
        self.assertEqual(b['b'], None)

    def test_delitem_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = benedict(d)
        del b['a.b']
        self.assertEqual(b['a'], {})
        del b['a']
        self.assertEqual(b['a'], None)

    def test_delitem_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = benedict(d)
        del b['a.c']
        self.assertEqual(b['a'], { 'b': 1 })

    def test_delitem_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                    'd': 2,
                },
            }
        }
        b = benedict(d)
        del b['a.b.c']
        self.assertEqual(b['a.b'], { 'd':2 })
        del b['a.b.d']
        self.assertEqual(b['a.b'], {})
        del b['a.b']
        self.assertEqual(b['a.b'], None)

    def test_delitem_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                    'd': 2,
                },
            }
        }
        b = benedict(d)
        del b['a.b.c.d']
        self.assertEqual(b['a.b.c'], 1)

    def test_setdefault_with_1_key(self):
        d = {
            'a': None,
            'b': 0,
            'c': 1,
        }
        b = benedict(d)
        b.setdefault('a', 2)
        b.setdefault('b', 2)
        b.setdefault('c', 2)
        b.setdefault('d', 2)
        self.assertEqual(b['a'], None)
        self.assertEqual(b['b'], 0)
        self.assertEqual(b['c'], 1)
        self.assertEqual(b['d'], 2)

    def test_setdefault_with_2_keys(self):
        d = {
            'a': {
                'a': None,
                'b': 0,
                'c': 1,
            },
        }
        b = benedict(d)
        b.setdefault('a.a', 2)
        b.setdefault('a.b', 2)
        b.setdefault('a.c', 2)
        b.setdefault('a.d', 2)
        self.assertEqual(b['a.a'], None)
        self.assertEqual(b['a.b'], 0)
        self.assertEqual(b['a.c'], 1)
        self.assertEqual(b['a.d'], 2)

    def test_setdefault_with_3_keys(self):
        d = {
            'a': {
                'b': {
                    'a': None,
                    'b': 0,
                    'c': 1,
                },
            },
        }
        b = benedict(d)
        b.setdefault('a.b.a', 2)
        b.setdefault('a.b.b', 2)
        b.setdefault('a.b.c', 2)
        b.setdefault('a.b.d', 2)
        self.assertEqual(b['a.b.a'], None)
        self.assertEqual(b['a.b.b'], 0)
        self.assertEqual(b['a.b.c'], 1)
        self.assertEqual(b['a.b.d'], 2)


class BenedictUtilityDictTestCase(unittest.TestCase):

    def test_get_bool_default(self):
        d = {
            'n': None,
        }
        b = benedict(d)
        self.assertTrue(b.get_bool('n', True))
        self.assertFalse(b.get_bool('n', False))
        self.assertTrue(b.get_bool('d1', True))
        self.assertFalse(b.get_bool('d2', False))

    def test_get_bool_with_bool_values(self):
        d = {
            'b1': True,
            'b2': False,
        }
        b = benedict(d)
        self.assertTrue(b.get_bool('b1'))
        self.assertFalse(b.get_bool('b2'))

    def test_get_bool_with_int_values(self):
        d = {
            'i0': 0,
            'i1': 1,
            'i2': 2,
        }
        b = benedict(d)
        self.assertFalse(b.get_bool('i0'))
        self.assertTrue(b.get_bool('i1'))
        self.assertTrue(b.get_bool('i2', True))
        self.assertFalse(b.get_bool('i2', False))

    def test_get_bool_with_str_values(self):
        d = {
            't1': '1',
            't2': 'YES',
            't3': 'True',
            'f1': '0',
            'f2': 'NO',
            'f3': 'False',
        }
        b = benedict(d)
        self.assertTrue(b.get_bool('t1'))
        self.assertTrue(b.get_bool('t2'))
        self.assertTrue(b.get_bool('t3'))
        self.assertFalse(b.get_bool('f1'))
        self.assertFalse(b.get_bool('f2'))
        self.assertFalse(b.get_bool('f3'))

    def test_get_bool_list(self):
        d = {
            'a': '1,YES,True,0,NO,False,XXX',
            'b': '1;YES;True;0;NO;False;XXX',
            'c': ['1', 'YES', True, 0, 'NO', 'False', 'XXX']
        }
        b = benedict(d)
        self.assertEqual(b.get_bool_list('a'), [True, True, True, False, False, False, None])
        self.assertEqual(b.get_bool_list('b'), [None])
        self.assertEqual(b.get_bool_list('b', separator=';'), [True, True, True, False, False, False, None])
        self.assertEqual(b.get_bool_list('c'), [True, True, True, False, False, False, None])
        self.assertEqual(b.get_bool_list('d', default=[False]), [False])

    def test_get_datetime_default(self):
        now = datetime.now()
        d = {
            'a': None,
        }
        b = benedict(d)
        self.assertEqual(b.get_datetime('a', now), now)
        self.assertEqual(b.get_datetime('b', now), now)

    def test_get_datetime_with_datetime_value(self):
        now = datetime.now()
        d = {
            'a': now,
        }
        b = benedict(d)
        self.assertEqual(b.get_datetime('a'), now)

    def test_get_datetime_with_valid_format(self):
        d = {
            'a': '2019-05-01',
        }
        b = benedict(d)
        r = datetime(2019, 5, 1, 0, 0)
        self.assertEqual(b.get_datetime('a', format='%Y-%m-%d'), r)

    def test_get_datetime_with_invalid_format(self):
        now = datetime.now()
        d = {
            'a': '2019-05-01',
        }
        b = benedict(d)
        r = datetime(2019, 5, 1, 0, 0)
        self.assertEqual(b.get_datetime('a', format='%Y/%m/%d'), None)
        self.assertEqual(b.get_datetime('a', now, format='%Y/%m/%d',), now)

    def test_get_datetime_without_format(self):
        d = {
            'a': '2019-05-01',
        }
        b = benedict(d)
        r = datetime(2019, 5, 1, 0, 0)
        self.assertEqual(b.get_datetime('a'), r)

    def test_get_datetime_list(self):
        d = {
            'a': ['2019-05-01', '2018-12-31', 'Hello World'],
            'b': '2019-05-01,2018-12-31',
        }
        b = benedict(d)
        self.assertEqual(b.get_datetime_list('a'), [datetime(2019, 5, 1, 0, 0), datetime(2018, 12, 31, 0, 0), None])
        self.assertEqual(b.get_datetime_list('b'), [datetime(2019, 5, 1, 0, 0), datetime(2018, 12, 31, 0, 0)])

    def test_get_decimal(self):
        d = {
            'a': 1,
            'b': True,
            'c': Decimal('4.25'),
        }
        b = benedict(d)
        self.assertEqual(b.get_decimal('a'), Decimal('1.0'))
        self.assertEqual(b.get_decimal('b'), Decimal('0.0'))
        self.assertEqual(b.get_decimal('b', Decimal('2.5')), Decimal('2.5'))
        self.assertEqual(b.get_decimal('c'), Decimal('4.25'))

    def test_get_decimal_with_options(self):
        d = {
            'a': Decimal('0.25'),
            'b': Decimal('0.35'),
        }
        b = benedict(d)
        o = [Decimal('0.0'), Decimal('0.25'), Decimal('0.5'), Decimal('0.75'), Decimal('1.0')]
        self.assertEqual(b.get_decimal('a', Decimal('0.5'), options=o), Decimal('0.25'))
        self.assertEqual(b.get_decimal('b', Decimal('0.5'), options=o), Decimal('0.5'))

    def test_get_decimal_list(self):
        d = {
            'a': ['0.0', '0.5', '1.0', 'Hello World'],
            'b': '0.0,0.5,1.0',
        }
        b = benedict(d)
        self.assertEqual(b.get_decimal_list('a'), [Decimal('0.0'), Decimal('0.5'), Decimal('1.0'), None])
        self.assertEqual(b.get_decimal_list('b'), [Decimal('0.0'), Decimal('0.5'), Decimal('1.0')])

    def test_get_dict(self):
        d = {
            'a': { 'x':1, 'y':2 },
            'b': {},
        }
        b = benedict(d)
        self.assertEqual(b.get_dict('a'), { 'x':1, 'y':2 })
        self.assertEqual(b.get_dict('b'), {})
        self.assertEqual(b.get_dict('b', { 'default':True }), {})
        self.assertEqual(b.get_dict('c'), {})
        self.assertEqual(b.get_dict('c', { 'default':True }), { 'default':True })

    def test_get_dict_from_json(self):
        d = {
            'a': '{"numbers": ["0", "1", "2", "3", "4"], "letters": ["a", "b", "c", "d", "e"]}',
            'b': '["0", "1", "2", "3", "4"]',
            'c': '{}',
            'd': '[]',
            'e': '',
            'f': '{"invalid::json"}'
        }
        b = benedict(d)
        self.assertEqual(b.get_dict('a'), { 'numbers': ['0', '1', '2', '3', '4'], 'letters': ['a', 'b', 'c', 'd', 'e'] })
        self.assertEqual(b.get_dict('b'), {})
        self.assertEqual(b.get_dict('c'), {})
        self.assertEqual(b.get_dict('c', { 'default':True }), {})
        self.assertEqual(b.get_dict('d', { 'default':True }), { 'default':True })
        self.assertEqual(b.get_dict('e'), {})
        self.assertEqual(b.get_dict('f'), {})
        self.assertEqual(b.get_dict('g', { 'default':True }), { 'default':True })

    def test_get_float(self):
        d = {
            'a': 1.0,
            'b': True,
            'c': float(4.25),
        }
        b = benedict(d)
        self.assertEqual(b.get_float('a'), float(1.0))
        self.assertEqual(b.get_float('b'), float(0.0))
        self.assertEqual(b.get_float('b', float(2.5)), float(2.5))
        self.assertEqual(b.get_float('c'), float(4.25))

    def test_get_float_with_options(self):
        d = {
            'a': float(0.25),
            'b': float(0.35),
        }
        b = benedict(d)
        o = [float(0.0), float(0.25), float(0.5), float(0.75), float(1.0)]
        self.assertEqual(b.get_float('a', float(0.5), options=o), float(0.25))
        self.assertEqual(b.get_float('b', float(0.5), options=o), float(0.5))

    def test_get_float_list(self):
        d = {
            'a': ['0.0', '0.5', '1.0', 'Hello World'],
            'b': '0.0,0.5,1.0',
        }
        b = benedict(d)
        self.assertEqual(b.get_float_list('a'), [0.0, 0.5, 1.0, None])
        self.assertEqual(b.get_float_list('b'), [0.0, 0.5, 1.0])

    def test_get_int(self):
        d = {
            'a': 1,
            'b': None,
            'c': int(4),
            'd': True,
            'e': False,
            'f': '3',
            'g': '3.5',
        }
        b = benedict(d)
        self.assertEqual(b.get_int('a'), 1)
        self.assertEqual(b.get_int('b'), 0)
        self.assertEqual(b.get_int('b', 2), 2)
        self.assertEqual(b.get_int('c'), 4)
        self.assertEqual(b.get_int('d', 2), 1)
        self.assertEqual(b.get_int('e', 2), 0)
        self.assertEqual(b.get_int('f', 2), 3)
        self.assertEqual(b.get_int('g', 2), 2)

    def test_get_int_with_options(self):
        d = {
            'a': 25,
            'b': 35,
        }
        b = benedict(d)
        o = [0, 25, 50, 75, 100]
        self.assertEqual(b.get_int('a', 50, options=o), 25)
        self.assertEqual(b.get_int('b', 50, options=o), 50)

    def test_get_int_list(self):
        d = {
            'a': ['0', '1', '2', 'Hello World'],
            'b': '0,1,2',
        }
        b = benedict(d)
        self.assertEqual(b.get_int_list('a'), [0, 1, 2, None])
        self.assertEqual(b.get_int_list('b'), [0, 1, 2])

    def test_get_list(self):
        d = {
            'a': (0, 1, 2, 3, ),
            'b': [0, 1, 2, 3],
            'c': [],
            'd': '{}',
            'e': '[]',
            'f': '',

        }
        b = benedict(d)
        self.assertEqual(b.get_list('a'), [0, 1, 2, 3])
        self.assertEqual(b.get_list('b'), [0, 1, 2, 3])
        self.assertEqual(b.get_list('c'), [])
        self.assertEqual(b.get_list('c', [0]), [])
        self.assertEqual(b.get_list('d'), [])
        self.assertEqual(b.get_list('e'), [])
        self.assertEqual(b.get_list('f'), [])
        self.assertEqual(b.get_list('g', [0]), [0])

    def test_get_list_from_json(self):
        d = {
            'a': '{"numbers": ["0", "1", "2", "3", "4"], "letters": ["a", "b", "c", "d", "e"]}',
            'b': '["0", "1", "2", "3", "4"]',
            'c': '[]',
        }
        b = benedict(d)
        self.assertEqual(b.get_list('a'), [])
        self.assertEqual(b.get_list('b'), ['0', '1', '2', '3', '4'])
        self.assertEqual(b.get_list('c'), [])
        self.assertEqual(b.get_list('c', [0]), [])
        self.assertEqual(b.get_list('d', [0]), [0])

    def test_get_list_with_separator(self):
        d = {
            'a': '0,1,2,3,4',
            'b': '5|6|7|8|9',
            'c': '',
        }
        b = benedict(d)
        self.assertEqual(b.get_list('a', separator=','), ['0', '1', '2', '3', '4'])
        self.assertEqual(b.get_list('b', separator='|'), ['5', '6', '7', '8', '9'])
        self.assertEqual(b.get_list('b'), ['5|6|7|8|9'])
        self.assertEqual(b.get_list('c', separator=','), [])
        self.assertEqual(b.get_list('d', separator=','), [])
        self.assertEqual(b.get_list('e', [0], separator=','), [0])

    def test_get_slug(self):
        d = {
            'a': ' Hello World ',
            'b': 1,
        }
        b = benedict(d)
        self.assertEqual(b.get_slug('a'), 'hello-world')
        self.assertEqual(b.get_slug('b', 'none'), '1')
        self.assertEqual(b.get_slug('c', 'none'), 'none')

    def test_get_slug_with_options(self):
        d = {
            'a': 'Sunday',
            'b': 'Noneday',
        }
        b = benedict(d)
        self.assertEqual(b.get_slug('a', options=['sunday', 'saturday']), 'sunday')
        self.assertEqual(b.get_slug('b', options=['sunday', 'saturday'], default='saturday'), 'saturday')
        self.assertEqual(b.get_slug('c', options=['sunday', 'saturday'], default='saturday'), 'saturday')

    def test_get_slug_list(self):
        d = {
            'a': ['Hello World', ' See you later ', 99.9],
            'b': 'Hello World, See you later, 99.9',
        }
        b = benedict(d)
        self.assertEqual(b.get_slug_list('a'), ['hello-world', 'see-you-later', '99-9'])
        self.assertEqual(b.get_slug_list('b'), ['hello-world', 'see-you-later', '99-9'])

    def test_get_str(self):
        d = {
            'a': 'Hello World',
            'b': 1,
        }
        b = benedict(d)
        self.assertEqual(b.get_str('a'), 'Hello World')
        self.assertEqual(b.get_str('b'), '1')

    def test_get_str_list(self):
        d = {
            'a': ['Hello World', 'See you later', 99.9],
            'b': 'Hello World,See you later,99.9',
        }
        b = benedict(d)
        self.assertEqual(b.get_str_list('a'), ['Hello World', 'See you later', '99.9'])
        self.assertEqual(b.get_str_list('b'), ['Hello World', 'See you later', '99.9'])

    def test_get_str_with_options(self):
        d = {
            'a': 'Sunday',
            'b': 'Noneday',
        }
        b = benedict(d)
        self.assertEqual(b.get_str('a', options=['Sunday', 'Saturday']), 'Sunday')
        self.assertEqual(b.get_str('b', options=['Sunday', 'Saturday'], default='Saturday'), 'Saturday')
        self.assertEqual(b.get_str('c', options=['Sunday', 'Saturday'], default='Saturday'), 'Saturday')
