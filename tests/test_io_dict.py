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
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.json'
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
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_json(filepath))

    # YAML
# TOML

    def test_from_toml_with_valid_data(self):
        j = """
            a = 1

            [b]
            c = 3
            d = 4
        """
        # static method
        d = IODict.from_toml(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})
        # constructor
        d = IODict(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

    def test_from_toml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_toml(j)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(j)

    def test_from_toml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.toml')
        # static method
        d = IODict.from_toml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_toml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.toml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_toml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_toml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.toml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_toml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_toml_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.toml'
        # static method
        d = IODict.from_toml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_toml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_toml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_from_toml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_toml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_to_toml(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        s = d.to_toml()
        self.assertEqual(d, IODict.from_toml(s))

    def test_to_toml_file(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        filepath = self.output_path('test_to_toml_file.toml')
        s = d.to_toml(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_toml(filepath))

# XML

    def test_from_xml_with_valid_data(self):
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
        d = IODict.from_xml(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d.get('root'), { 'a':'1', 'b':{ 'c':'3', 'd':'4' },})
        # constructor
        d = IODict(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d.get('root'), { 'a':'1', 'b':{ 'c':'3', 'd':'4' },})

    def test_from_xml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_xml(j)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(j)

    def test_from_xml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.xml')
        # static method
        d = IODict.from_xml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.xml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_xml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.xml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    # def test_from_xml_with_valid_url_valid_content(self):
    #     url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.xml'
    #     # static method
    #     d = IODict.from_xml(url)
    #     self.assertTrue(isinstance(d, dict))
    #     # constructor
    #     d = IODict(url)
    #     self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_from_xml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_to_xml(self):
        d = IODict({
            'root': {
                'x': '7',
                'y': '8',
                'z': '9',
                'a': '1',
                'b': '2',
                'c': '3',
            },
        })
        s = d.to_xml()
        self.assertEqual(d, IODict.from_xml(s))

    def test_to_xml_file(self):
        d = IODict({
            'root': {
                'x': '7',
                'y': '8',
                'z': '9',
                'a': '1',
                'b': '2',
                'c': '3',
            },
        })
        filepath = self.output_path('test_to_xml_file.xml')
        s = d.to_xml(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_xml(filepath))

# YAML

    def test_from_yaml_with_valid_data(self):
        j = """
            a: 1
            b:
              c: 3
              d: 4
        """
        # static method
        d = IODict.from_yaml(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})
        # constructor
        d = IODict(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

    def test_from_yaml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_yaml(j)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(j)

    def test_from_yaml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.yml')
        # static method
        d = IODict.from_yaml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.yml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_yaml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.yml')
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(filepath)

    def test_from_yaml_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.yml'
        # static method
        d = IODict.from_yaml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_from_yaml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            d = IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            d = IODict(url)

    def test_to_yaml(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        s = d.to_yaml()
        self.assertEqual(d, IODict.from_yaml(s))

    def test_to_yaml_file(self):
        d = IODict({
            'x': 7,
            'y': 8,
            'z': 9,
            'a': 1,
            'b': 2,
            'c': 3,
        })
        filepath = self.output_path('test_to_yaml_file.yml')
        s = d.to_yaml(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_yaml(filepath))
