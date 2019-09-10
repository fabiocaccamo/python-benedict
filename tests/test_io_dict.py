# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict

import os
import shutil
import unittest


class IODictTestCase(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.output_path(filepath=''))

    @staticmethod
    def input_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'input/{}'.format(filepath))

    @staticmethod
    def output_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'output/{}'.format(filepath))

    # JSON

    def test_from_json_with_valid_data(self):
        j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor
        d = IODict(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    def test_from_json_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_json(j)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(j)

    def test_from_json_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.json')
        # static method
        d = IODict.from_json(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.json')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_json_with_invalid_file(self):
        filepath = self.input_path('invalid-file.json')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_json_with_valid_url_valid_content(self):
        url = 'https://jsonplaceholder.typicode.com/users'
        # static method
        d = IODict.from_json(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_from_json_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_to_json(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        s = d.to_json(sort_keys=True)
        self.assertEqual(s, '{"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9}')

    def test_to_json_file(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        filepath = self.output_path('test_to_json_file.json')
        s = d.to_json(filepath=filepath, sort_keys=True)
        self.assertEqual(d, IODict.from_json(filepath))

    # def test_from_query_string(self):
    #     pass

    # def test_from_query_string_file(self):
    #     pass

    # def test_from_query_string_url(self):
    #     pass

    # def test_from_toml_string(self):
    #     pass

    # def test_from_toml_file(self):
    #     pass

    # def test_from_toml_url(self):
    #     pass

    # def test_from_xml_string(self):
    #     pass

    # def test_from_xml_file(self):
    #     pass

    # def test_from_xml_url(self):
    #     pass

    # def test_from_yaml_string(self):
    #     pass

    # def test_from_yaml_file(self):
    #     pass

    # def test_from_yaml_url(self):
    #     pass

    # def test_to_base64(self):
    #     pass

    # def test_to_base64_file(self):
    #     pass

    # def test_to_query_string(self):
    #     pass

    # def test_to_query_string_file(self):
    #     pass

    # def test_to_toml(self):
    #     pass

    # def test_to_toml_file(self):
    #     pass

    # def test_to_xml(self):
    #     pass

    # def test_to_xml_file(self):
    #     pass

    # def test_to_yaml(self):
    #     pass

    # def test_to_yaml_file(self):
    #     pass
