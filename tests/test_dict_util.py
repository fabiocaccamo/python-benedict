# -*- coding: utf-8 -*-

from benedict.utils import dict_util as u
from decimal import Decimal

import datetime as dt
import unittest


class dict_util_test_case(unittest.TestCase):

    def test_clean(self):
        i = {
            'a': {},
            'b': { 'x': 1 },
            'c': [],
            'd': [0, 1],
            'e': 0.0,
            'f': '',
            'g': None,
            'h': '0'
        }

        o = i.copy()
        u.clean(o)
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'h': '0',
        }
        self.assertEqual(o, r)

        o = i.copy()
        u.clean(o, collections=False)
        r = {
            'a': {},
            'b': { 'x': 1 },
            'c': [],
            'd': [0, 1],
            'e': 0.0,
            'h': '0'
        }
        self.assertEqual(o, r)

        o = i.copy()
        u.clean(o, strings=False)
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'f': '',
            'h': '0',
        }
        self.assertEqual(o, r)

    def test_clone(self):
        i = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        o = u.clone(i)
        self.assertEqual(type(i), type(o))
        self.assertEqual(i, o)
        self.assertFalse(i is o)
        o['a']['b']['c'] = 2
        self.assertEqual(i['a']['b']['c'], 1)
        self.assertEqual(o['a']['b']['c'], 2)

    def test_dump(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        r = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        o = u.dump(d)
        self.assertEqual(o, r)

    def test_dump_with_datetime(self):
        d = {
            'datetime': dt.datetime(2019, 6, 11),
        }
        r = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        o = u.dump(d)
        self.assertEqual(o, r)

    def test_dump_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        r = """{
    "decimal": "1.75"
}"""
        o = u.dump(d)
        self.assertEqual(o, r)

    def test_filter(self):
        i = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        with self.assertRaises(ValueError):
            f = u.filter(i, True)
        o = u.filter(i, lambda key, val: isinstance(val, int))
        r = {
            'a': 1,
            'b': 2,
            'f': 6,
            'g': 7,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_flatten(self):
        i = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'e': 3,
                    'f': 4,
                    'g': {
                        'h': 5,
                    }
                }
            },
        }
        o = u.flatten(i)
        r = {
            'a': 1,
            'b': 2,
            'c_d_e': 3,
            'c_d_f': 4,
            'c_d_g_h': 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_custom_separator(self):
        i = {
            'a': 1,
            'b': 2,
            'c': {
                'd': {
                    'e': 3,
                    'f': 4,
                    'g': {
                        'h': 5,
                    }
                }
            },
        }
        o = u.flatten(i, separator='/')
        r = {
            'a': 1,
            'b': 2,
            'c/d/e': 3,
            'c/d/f': 4,
            'c/d/g/h': 5,
        }
        self.assertEqual(o, r)

    def test_flatten_with_key_conflict(self):
        i = {
            'a': 1,
            'b': 2,
            'c': {
                'd': 3,
            },
            'c_d': 4,
            'd_e': 5,
            'd': {
                'e': 6,
            }
        }
        o = u.flatten(i)
        r = {
            'a': 1,
            'b': 2,
            'c_d': 4,
            'd_e': 5,
        }
        self.assertEqual(o, r)

    def test_invert_with_unique_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        o = u.invert(i)
        r = {
            1: ['a'],
            2: ['b'],
            3: ['c'],
            4: ['d'],
            5: ['e'],
        }
        self.assertEqual(o, r)

    def test_invert_with_flat_unique_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        o = u.invert(i, flat=True)
        r = {
            1: 'a',
            2: 'b',
            3: 'c',
            4: 'd',
            5: 'e',
        }
        self.assertEqual(o, r)

    def test_invert_with_multiple_values(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 1,
            'e': 2,
            'f': 3,
        }
        o = u.invert(i)
        self.assertTrue('a' and 'd' in o[1])
        self.assertTrue('b' and 'e' in o[2])
        self.assertTrue('c' and 'f' in o[3])

    def test_items_sorted_by_keys(self):
        i = {
            'y': 3,
            'a': 6,
            'f': 9,
            'z': 4,
            'x': 1,
        }
        o = u.items_sorted_by_keys(i)
        r = [
            ('a', 6,),
            ('f', 9,),
            ('x', 1,),
            ('y', 3,),
            ('z', 4,),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_keys_reverse(self):
        i = {
            'y': 3,
            'a': 6,
            'f': 9,
            'z': 4,
            'x': 1,
        }
        o = u.items_sorted_by_keys(i, reverse=True)
        r = [
            ('z', 4,),
            ('y', 3,),
            ('x', 1,),
            ('f', 9,),
            ('a', 6,),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_values(self):
        i = {
            'a': 3,
            'b': 6,
            'c': 9,
            'e': 4,
            'd': 1,
        }
        o = u.items_sorted_by_values(i)
        r = [
            ('d', 1,),
            ('a', 3,),
            ('e', 4,),
            ('b', 6,),
            ('c', 9,),
        ]
        self.assertEqual(o, r)

    def test_items_sorted_by_values_reverse(self):
        i = {
            'a': 3,
            'b': 6,
            'c': 9,
            'e': 4,
            'd': 1,
        }
        o = u.items_sorted_by_values(i, reverse=True)
        r = [
            ('c', 9,),
            ('b', 6,),
            ('e', 4,),
            ('a', 3,),
            ('d', 1,),
        ]
        self.assertEqual(o, r)

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
        o = u.keypaths(i)
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
        o = u.keypaths(i, separator='/')
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
            o = u.keypaths(i, separator=None)

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
        o = u.keypaths(i)
        r = [
            'False',
            'False.False',
            'None',
            'None.None',
            'True',
            'True.True',
        ]
        self.assertEqual(o, r)

    def test_merge_with_flatten_dict(self):
        d = {
            'a': 1,
            'b': 1,
        }
        m = {
            'b': 2,
            'c': 3,
        }
        u.merge(d, m)
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
        u.merge(d, a, b, c)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        self.assertEqual(d, r)

    def test_merge_with_nested_dict(self):
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
        m = {
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
        u.merge(d, m)
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

    def test_move(self):
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
        }
        u.move(d, 'a', 'd')
        r = {
            'b': {
                'x': 2,
                'y': 2,
            },
            'c': {
                'x': 3,
                'y': 3,
            },
            'd': {
                'x': 1,
                'y': 1,
            },
        }
        self.assertEqual(d, r)

    def test_move_with_same_key(self):
        d = {
            'a': 1,
            'b': 2,
        }
        u.move(d, 'a', 'a')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_single_key(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        u.remove(d, 'c')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_args(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        u.remove(d, 'c', 'd', 'e')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(d, r)

    def test_remove_with_multiple_keys_as_list(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        u.remove(d, ['c', 'd', 'e'])
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(d, r)

    def test_standardize(self):
        d = {
            'CamelCase': 1,
            'CamelCamelCase': 1,
            'Camel2Camel2Case': 1,
            'getHTTPResponseCode': 1,
            'get2HTTPResponseCode': 1,
            'HTTPResponseCode': 1,
            'HTTPResponseCodeXYZ': 1,
            ' LocationCoordinates ': {
                'Lat. ': 0.0,
                'Lng. ': 0.0,
            },
        }
        u.standardize(d)
        r = {
            'camel_case': 1,
            'camel_camel_case': 1,
            'camel2_camel2_case': 1,
            'get_http_response_code': 1,
            'get2_http_response_code': 1,
            'http_response_code': 1,
            'http_response_code_xyz': 1,
            'location_coordinates': {
                'lat': 0.0,
                'lng': 0.0,
            },
        }
        # print(u.dump(d))
        # print(u.dump(r))
        self.assertEqual(d, r)

    def test_subset_with_keys_as_args(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        o = u.subset(i, 'c', 'f', 'x')
        r = {
            'c': 3,
            'f': 6,
            'x': None,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_subset_with_keys_as_list(self):
        i = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        o = u.subset(i, ['c', 'f', 'x'])
        r = {
            'c': 3,
            'f': 6,
            'x': None,
        }
        self.assertFalse(i is o)
        self.assertEqual(o, r)

    def test_swap(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        u.swap(d, 'a', 'b')
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
        u.swap(d, 'a', 'a')
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
            u.swap(d, 'a', 'd')

    def test_traverse(self):
        i = {
            'a': {
                'x': 2,
                'y': 3,
                'z': {
                    'ok': 5,
                }
            },
            'b': {
                'x': 7,
                'y': 11,
                'z': {
                    'ok': 13,
                }
            },
            'c': {
                'x': 17,
                'y': 19,
                'z': {
                    'ok': 23,
                }
            },
        }
        o = u.clone(i)
        with self.assertRaises(ValueError):
            u.traverse(o, True)
        def f(parent, key, value):
            if not isinstance(value, dict):
                parent[key] = (value + 1)
        u.traverse(o, f)
        r = {
            'a': {
                'x': 3,
                'y': 4,
                'z': {
                    'ok': 6,
                }
            },
            'b': {
                'x': 8,
                'y': 12,
                'z': {
                    'ok': 14,
                }
            },
            'c': {
                'x': 18,
                'y': 20,
                'z': {
                    'ok': 24,
                }
            },
        }
        self.assertEqual(o, r)

    def test_unique(self):
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
                'x': 1,
                'y': 1,
            },
            'd': {
                'x': 1,
            },
            'e': {
                'x': 1,
                'y': 1,
                'z': 1,
            },
            'f': {
                'x': 2,
                'y': 2,
            },
        }
        u.unique(d)
        rv = [
            {
                'x': 1,
                'y': 1,
            },
            {
                'x': 2,
                'y': 2,
            },
            {
                'x': 1,
            },
            {
                'x': 1,
                'y': 1,
                'z': 1,
            },
        ]
        self.assertEqual(len(d.keys()), len(rv))
        self.assertTrue(all([value in rv for value in d.values()]))
