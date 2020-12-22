# -*- coding: utf-8 -*-

from benedict import benedict

import json
import unittest


class github_issue_0046_test_case(unittest.TestCase):

    """
    https://github.com/fabiocaccamo/python-benedict/issues/46

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0046
    """
    def test_json_dumps_with_cloned_instance(self):
        d = {
            'id': '37e4f6e876',
            'meta': {
                'data': {
                    'category': 'category0',
                    'id': 'data_id',
                    'title': 'A title'
                },
                'id': '37e4f6e876',
                'k0': {
                    'ka': {
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'value3',
                        'key4': True
                    },
                    'kb': {
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'value3',
                        'key4': True
                    },
                    'kc': {
                        'extra_key2': 'value2',
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'value3',
                        'key4': True
                    },
                    'kd': {
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'value3',
                        'key4': True
                    },
                    'ke': {
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'value3',
                        'key4': True
                    },
                    'kf': {
                        'key1': '',
                        'key2': 'value2',
                        'key3': 'separated',
                        'key4': True
                    }
                },
                'language': 'en',
                'name': 'name_value'
            }
        }
        keypaths = ['id', 'meta.k0.kc', 'meta.language']
        d = benedict(d)
        d_new = benedict()
        d_new = d.subset(keypaths)

        d_new_raw = {'id': '37e4f6e876', 'meta': {'k0': {'kc': {'extra_key2': 'value2', 'key1': '', 'key2': 'value2', 'key3': 'value3', 'key4': True}}, 'language': 'en'}}
        d_new_json = json.dumps(d_new_raw, sort_keys=True)
        self.assertEqual(d_new, d_new_raw)
        self.assertEqual(d_new.to_json(), d_new_json)

        d_new2 = d_new.clone()
        self.assertEqual(d_new, d_new2)
        self.assertEqual(d_new.to_json(), d_new2.to_json())
