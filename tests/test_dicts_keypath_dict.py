# -*- coding: utf-8 -*-

from benedict.dicts import KeypathDict

import unittest


class KeypathDictTestCase(unittest.TestCase):

    # def test_list_as_key(self):
    #     keys = ['a', 'b', 'c']
    #     d = {}
    #     d[keys] = 1
    #     print(d)
    #     print(d[keys])

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
        b = KeypathDict.fromkeys(k)
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
        # self.assertEqual(type(b), benedict)

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
        b = KeypathDict.fromkeys(k, True)
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
        # self.assertEqual(type(b), benedict)

    def test_get_with_1_valid_key(self):
        d = {
            'a': 1,
            1: 1
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('a', 2), 1)
        self.assertEqual(b.get(1, 2), 1)

    def test_get_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('b', 2), 2)

    def test_get_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
            0: 0,
        }
        b = KeypathDict(d)
        self.assertEqual(b.get(None, 1), None)
        self.assertEqual(b.get(False, True), False)
        self.assertEqual(b.get(True, True), True)
        self.assertEqual(b.get(0, 1), 0)

    def test_get_with_keys_list(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                    'd': 2,
                },
            },
        }
        b = KeypathDict(d)
        self.assertEqual(b.get(['a.b.c']), 1)
        self.assertEqual(b.get(['a.b', 'c']), 1)
        self.assertEqual(b.get(['a', 'b.c']), 1)
        self.assertEqual(b.get(['a', 'b', 'c']), 1)
        self.assertEqual(b.get(['a', 'b', 'd']), 2)
        self.assertEqual(b.get(['a', 'b', 'e']), None)

    def test_getitem_with_1_valid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        self.assertEqual(b['a'], 1)

    def test_getitem_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b['b']
            print(val)

    def test_getitem_with_1_not_str_key(self):
        d = {
            None: None,
            False: False,
            # 0: 0,
        }
        b = KeypathDict(d)
        self.assertEqual(b[None], None)
        self.assertEqual(b[False], False)
        with self.assertRaises(KeyError):
            val = b[True]
            print(val)

        self.assertEqual(b[0], 0)

    def test_get_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('a.b', 2), 1)

    def test_get_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('b.a', 2), 2)

    def test_getitem_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b['a.b'], 1)

    def test_getitem_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b['b.a']
            print(val)

    def test_get_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('a.b.c', 2), 1)

    def test_get_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b.get('c.b.a', 2), 2)

    def test_getitem_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = KeypathDict(d)
        self.assertEqual(b['a.b.c'], 1)

    def test_getitem_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b['c.b.a']
            print(val)

    # def test_get_item_with_keys_list(self):
    #     d = {
    #         'a': {
    #             'b': {
    #                 'c': 1,
    #                 'd': 2,
    #             },
    #         },
    #     }
    #     b = KeypathDict(d)
    #     self.assertEqual(b['a.b.c'], 1)
    #     self.assertEqual(b['a.b', 'c'], 1)
    #     self.assertEqual(b.get(['a', 'b.c']), 1)
    #     self.assertEqual(b.get(['a', 'b', 'c']), 1)
    #     self.assertEqual(b.get(['a', 'b', 'd']), 2)
    #     self.assertEqual(b.get(['a', 'b', 'e']), None)

    def test_has_with_1_key(self):
        d = {
            'a': 0,
            'b': None,
            'c': {},
        }
        b = KeypathDict(d)
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
        b = KeypathDict(d)
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
        b = KeypathDict(d)
        self.assertTrue('a.b.c' in b)
        self.assertTrue('a.b.d' in b)
        self.assertTrue('a.b.e' in b)
        self.assertFalse('a.b.f' in b)
        self.assertFalse('b.f' in b)
        self.assertFalse('f' in b)

    def test_keypaths(self):
        d = {
            'x': {
                'y': True,
                'z': False,
            },
            'a': {
                'b': {
                    'c': 0,
                    'd': None,
                    'e': {},
                },
            },
        }
        b = KeypathDict(d)
        r = [
            'a',
            'a.b',
            'a.b.c',
            'a.b.d',
            'a.b.e',
            'x',
            'x.y',
            'x.z',
        ]
        self.assertEqual(b.keypaths(), r)

    def test_set_override_existing_item(self):
        d = {}
        b = KeypathDict(d)
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
        b = KeypathDict(d)
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
        b = KeypathDict(d)
        del b['a']
        with self.assertRaises(KeyError):
            del b['a']
        self.assertEqual(b.get('a'), None)

    def test_delitem_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b['b']
        self.assertEqual(b.get('b'), None)

    def test_delitem_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = KeypathDict(d)

        del b['a.b']
        with self.assertRaises(KeyError):
            del b['a.b']
        self.assertEqual(b.get('a'), {})

        del b['a']
        with self.assertRaises(KeyError):
            del b['a']
        self.assertEqual(b.get('a'), None)

    def test_delitem_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b['a.c']
        self.assertEqual(b.get('a'), { 'b': 1 })

    def test_delitem_with_3_valid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                    'd': 2,
                },
            }
        }
        b = KeypathDict(d)

        del b['a.b.c']
        with self.assertRaises(KeyError):
            del b['a.b.c']
        self.assertEqual(b.get('a.b'), { 'd':2 })

        del b['a.b.d']
        with self.assertRaises(KeyError):
            del b['a.b.d']
        self.assertEqual(b.get('a.b'), {})

        del b['a.b']
        with self.assertRaises(KeyError):
            del b['a.b']
        self.assertEqual(b.get('a.b'), None)

    def test_delitem_with_3_invalid_keys(self):
        d = {
            'a': {
                'b': {
                    'c': 1,
                    'd': 2,
                },
            }
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            del b['a.b.c.d']
        self.assertEqual(b.get('a.b.c'), 1)

    def test_pop_with_1_valid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        val = b.pop('a')
        self.assertEqual(val, 1)

    def test_pop_with_1_invalid_key(self):
        d = {
            'a': 1,
        }
        b = KeypathDict(d)
        with self.assertRaises(KeyError):
            val = b.pop('b')
        val = b.pop('b', False)
        self.assertFalse(val)

    def test_pop_with_2_valid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = KeypathDict(d)

        val = b.pop('a.b')
        with self.assertRaises(KeyError):
            val = b.pop('a.b')
        self.assertEqual(val, 1)

        val = b.pop('a')
        with self.assertRaises(KeyError):
            val = b.pop('a')
        self.assertEqual(val, {})

    def test_pop_with_2_invalid_keys(self):
        d = {
            'a': {
                'b': 1,
            }
        }
        b = KeypathDict(d)

        val = b.pop('a.c', 2)
        self.assertEqual(val, 2)
        with self.assertRaises(KeyError):
            val = b.pop('a.c')
        self.assertEqual(b.get('a'), { 'b': 1 })

        val = b.pop('x.y', 1)
        self.assertEqual(val, 1)
        with self.assertRaises(KeyError):
            val = b.pop('x.y')

    def test_setdefault_with_1_key(self):
        d = {
            'a': None,
            'b': 0,
            'c': 1,
        }
        b = KeypathDict(d)
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
        b = KeypathDict(d)
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
        b = KeypathDict(d)
        b.setdefault('a.b.a', 2)
        b.setdefault('a.b.b', 2)
        b.setdefault('a.b.c', 2)
        b.setdefault('a.b.d', 2)
        self.assertEqual(b['a.b.a'], None)
        self.assertEqual(b['a.b.b'], 0)
        self.assertEqual(b['a.b.c'], 1)
        self.assertEqual(b['a.b.d'], 2)

    def test_cast_existing_dict_with_keys_containing_dots_for_casting(self):
        # TODO
        pass

    def test_cast_existing_dict_with_keys_containing_dots_for_update(self):
        # TODO
        pass

