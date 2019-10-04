# -*- coding: utf-8 -*-

from benedict import benedict
from datetime import datetime
from decimal import Decimal

import unittest


class BenedictTestCase(unittest.TestCase):

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
        bd = benedict(d)
        bd.clean()
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'h': '0',
        }
        self.assertEqual(bd, r)

        bd = benedict(d)
        bd.clean(dicts=False)
        r = {
            'a': {},
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'h': '0'
        }
        self.assertEqual(bd, r)

        bd = benedict(d)
        bd.clean(lists=False)
        r = {
            'b': { 'x': 1 },
            'c': [],
            'd': [0, 1],
            'e': 0.0,
            'h': '0'
        }
        self.assertEqual(bd, r)

        bd = benedict(d)
        bd.clean(strings=False)
        r = {
            'b': { 'x': 1 },
            'd': [0, 1],
            'e': 0.0,
            'f': '',
            'h': '0',
        }
        self.assertEqual(bd, r)

    def test_clone(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = benedict(d)
        c = b.clone()
        self.assertEqual(b, c)
        self.assertFalse(c is b)
        c['a']['b']['c'] = 2
        self.assertEqual(b['a']['b']['c'], 1)
        self.assertEqual(c['a']['b']['c'], 2)

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

    def test_deepupdate_with_single_dict(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
        }
        bd = benedict(d)
        bd.deepupdate(a)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        self.assertEqual(bd, r)

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
        bd = benedict(d)
        bd.deepupdate(a, b, c)
        r = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
        }
        self.assertEqual(bd, r)

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
        bd = benedict(d)
        bd.deepupdate(a)
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
        self.assertEqual(bd, r)

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
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = benedict(d)
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

    def test_filter_with_parse(self):
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
        f = b.filter(lambda key, val: benedict(val).get_bool('ok'))
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

    def test_flatten(self):
        d = {
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
        b = benedict(d)
        f = b.flatten()
        r = {
            'a': 1,
            'b': 2,
            'c_d_e': 3,
            'c_d_f': 4,
            'c_d_g_h': 5,
        }
        self.assertEqual(f, r)
        self.assertTrue(isinstance(f, benedict))

    def test_flatten_with_custom_separator(self):
        d = {
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
        b = benedict(d)
        f = b.flatten(separator='|')
        r = {
            'a': 1,
            'b': 2,
            'c|d|e': 3,
            'c|d|f': 4,
            'c|d|g|h': 5,
        }
        self.assertEqual(f, r)
        self.assertFalse(b is f)

    def test_flatten_with_key_conflict(self):
        d = {
            'a': 1,
            'b': 2,
            'c_d': 4,
            'c': {
                'd': 3,
            },
        }
        b = benedict(d)
        f = b.flatten()
        r = {
            'a': 1,
            'b': 2,
            'c_d': 4,
        }
        self.assertEqual(f, r)
        self.assertFalse(b is f)

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

    def test_from_base64(self):
        j = 'eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9'
        # static method
        d = benedict.from_base64(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor
        d = benedict(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

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

    def test_from_toml(self):
        j = """
            a = 1

            [b]
            c = 3
            d = 4
        """
        # static method
        d = benedict.from_toml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})
        # constructor
        d = benedict(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

    def test_from_xml(self):
        j = """<?xml version="1.0" ?>
            <root>
                <a>1</a>
                <b>
                    <c>3</c>
                    <d>4</d>
                </b>
            </root>
        """
        # static method
        d = benedict.from_xml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d.get('root'), { 'a':'1', 'b':{ 'c':'3', 'd':'4' },})
        # constructor
        d = benedict(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d.get('root'), { 'a':'1', 'b':{ 'c':'3', 'd':'4' },})

    def test_from_yaml(self):
        j = """
            a: 1
            b:
              c: 3
              d: 4
        """
        # static method
        d = benedict.from_yaml(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})
        # constructor
        d = benedict(j)
        self.assertTrue(isinstance(d, benedict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

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
        # self.assertTrue(isinstance(b.get('b'), benedict))
        # self.assertTrue(isinstance(b.get('b.d'), benedict))
        # bb = b.get('b')
        # self.assertTrue(isinstance(bb.get('d'), benedict))

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
        # self.assertTrue(isinstance(b['b'], benedict))
        # self.assertTrue(isinstance(b['b.d'], benedict))
        # bb = b['b']
        # self.assertTrue(isinstance(bb['d'], benedict))

    def test_get_dict(self):
        d = {
            'a': {'x': 1, 'y': 2},
            'b': {},
        }
        b = benedict(d)
        # self.assertTrue(isinstance(b.get_dict('a'), benedict))
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
        # self.assertTrue(isinstance(l[0], benedict))
        # self.assertTrue(isinstance(l[1], benedict))
        # self.assertTrue(isinstance(l[2], benedict))
        # self.assertEqual(l[0].get('b.c'), 1)
        # self.assertEqual(l[1].get('b.c'), 2)
        # self.assertEqual(l[2].get('b.c'), 3)
        self.assertEqual(benedict(l[0]).get('b.c'), 1)
        self.assertEqual(benedict(l[1]).get('b.c'), 2)
        self.assertEqual(benedict(l[2]).get('b.c'), 3)

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
        i = benedict(b.get_list_item('a', index=1))
        # self.assertTrue(isinstance(i, benedict))
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
        # self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber('a.c')
        self.assertEqual(p, r)
        # self.assertTrue(isinstance(p, benedict))

        p = b.get_phonenumber('a.d')
        self.assertEqual(p, {})
        # self.assertTrue(isinstance(p, benedict))

    def test_invert(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        bd = benedict(d)
        i = bd.invert()
        r = {
            1: ['a'],
            2: ['b'],
            3: ['c'],
            4: ['d'],
            5: ['e'],
        }
        self.assertEqual(i, r)

    def test_invert_multiple_values(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 1,
            'e': 2,
            'f': 3,
        }
        bd = benedict(d)
        i = bd.invert()
        self.assertTrue('a' and 'd' in i[1])
        self.assertTrue('b' and 'e' in i[2])
        self.assertTrue('c' and 'f' in i[3])

    def test_invert_flat(self):
        d = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
        }
        bd = benedict(d)
        i = bd.invert(flat=True)
        r = {
            1: 'a',
            2: 'b',
            3: 'c',
            4: 'd',
            5: 'e',
        }
        self.assertEqual(i, r)

    def test_items_sorted_by_keys(self):
        d = {
            'y': 3,
            'a': 6,
            'f': 9,
            'z': 4,
            'x': 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_keys()
        self.assertEqual(items, [
            ('a', 6,),
            ('f', 9,),
            ('x', 1,),
            ('y', 3,),
            ('z', 4,),
        ])

    def test_items_sorted_by_keys_reverse(self):
        d = {
            'y': 3,
            'a': 6,
            'f': 9,
            'z': 4,
            'x': 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_keys(reverse=True)
        self.assertEqual(items, [
            ('z', 4,),
            ('y', 3,),
            ('x', 1,),
            ('f', 9,),
            ('a', 6,),
        ])

    def test_items_sorted_by_values(self):
        d = {
            'a': 3,
            'b': 6,
            'c': 9,
            'e': 4,
            'd': 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_values()
        self.assertEqual(items, [
            ('d', 1,),
            ('a', 3,),
            ('e', 4,),
            ('b', 6,),
            ('c', 9,),
        ])

    def test_items_sorted_by_values_reverse(self):
        d = {
            'a': 3,
            'b': 6,
            'c': 9,
            'e': 4,
            'd': 1,
        }
        bd = benedict(d)
        items = bd.items_sorted_by_values(reverse=True)
        self.assertEqual(items, [
            ('c', 9,),
            ('b', 6,),
            ('e', 4,),
            ('a', 3,),
            ('d', 1,),
        ])

    def test_merge_with_single_dict(self):
        d = {
            'a': 1,
            'b': 1,
        }
        a = {
            'b': 2,
            'c': 3,
        }
        d = benedict(d)
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
        d = benedict(d)
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
        d = benedict(d)
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
        # self.assertTrue(isinstance(b.pop('b.d'), benedict))

    def test_remove_with_key(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
        }
        b = benedict(d)
        b.remove('c')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keys_list(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = benedict(d)
        b.remove(['c', 'e', 'f', 'g', 'x', 'y', 'z'])
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keys_args(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = benedict(d)
        b.remove('c', 'e', 'f', 'g', 'x', 'y', 'z')
        r = {
            'a': 1,
            'b': 2,
        }
        self.assertEqual(b, r)

    def test_remove_with_keypath(self):
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

    # def test_setdefault(self):
    #     d = {
    #         'a': 1,
    #         'b': {
    #             'c': 2,
    #             'd': {
    #                 'e': 3,
    #             }
    #         }
    #     }
    #     b = benedict(d)
    #     self.assertTrue(isinstance(b.setdefault('b', 1), benedict))
    #     self.assertTrue(isinstance(b.setdefault('b.d', 1), benedict))

    def test_subset(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = benedict(d)
        f = b.subset(['c', 'f', 'x'])
        r = {
            'c': '4',
            'f': 6,
            'x': None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)

    def test_subset_with_keys_args(self):
        d = {
            'a': 1,
            'b': 2,
            'c': '4',
            'e': '5',
            'f': 6,
            'g': 7,
        }
        b = benedict(d)
        f = b.subset('c', 'f', 'x')
        r = {
            'c': '4',
            'f': 6,
            'x': None,
        }
        self.assertEqual(f, r)
        self.assertFalse(f is b)

    def test_subset_with_keypath(self):
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
