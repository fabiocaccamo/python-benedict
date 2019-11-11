# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict

import os
import shutil
import unittest


class io_dict_test_case(unittest.TestCase):

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

# BASE64

    def test_from_base64_with_valid_data(self):
        j = 'eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9'
        # j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = IODict.from_base64(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor
        d = IODict(j, format='base64')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor with subformat
        d = IODict(j, format='base64', subformat='json')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    def test_from_base64_with_valid_data_without_padding(self):
        j = 'eyJhIjogMSwgImIiOiAyLCAiYyI6IDMsICJkIjogNH0'
        # eyJhIjogMSwgImIiOiAyLCAiYyI6IDMsICJkIjogNH0=
        # j = '{"a": 1, "b": 2, "c": 3, "d": 4}'
        # static method
        d = IODict.from_base64(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, 'd': 4})
        # constructor
        d = IODict(j, format='base64')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, 'd': 4})

    def test_from_base64_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format='base64')

    def test_from_base64_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.base64')
        # static method
        d = IODict.from_base64(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='base64')
        self.assertTrue(isinstance(d, dict))

    def test_from_base64_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.json')
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path('valid-content.yml')
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)

    def test_from_base64_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.base64')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='base64')

    def test_from_base64_with_invalid_file(self):
        filepath = self.input_path('invalid-file.base64')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='base64')

    def test_from_base64_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.base64'
        # static method
        d = IODict.from_base64(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='base64')
        self.assertTrue(isinstance(d, dict))

    def test_from_base64_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='base64')

    def test_from_base64_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='base64')

    def test_to_base64(self):
        d = IODict({
            'a': 1,
            'b': 2,
            'c': 3,
        })
        s = d.to_base64(sort_keys=True)
        self.assertEqual(s, 'eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9')

    def test_to_base64_file(self):
        d = IODict({
            'a': 1,
            'b': 2,
            'c': 3,
        })
        filepath = self.output_path('test_to_base64_file.base64')
        d.to_base64(filepath=filepath, sort_keys=True)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_base64(filepath))

# CSV

    def test_from_csv_with_valid_data(self):
        s = """id,name,age,height,weight
1,Alice,20,62,120.6
2,Freddie,21,74,190.6
3,Bob,17,68,120.0
4,François,32,75,110.05
"""
        r = {
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        }
        # static method
        d = IODict.from_csv(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format='csv')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    # def test_from_csv_with_invalid_data(self):
    #     s = 'Lorem ipsum est in ea occaecat nisi officia.'
    #     # static method
    #     with self.assertRaises(ValueError):
    #         print(IODict.from_csv(s))
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(s, format='csv')

    def test_from_csv_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.csv')
        # static method
        d = IODict.from_csv(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='csv')
        self.assertTrue(isinstance(d, dict))

    # def test_from_csv_with_valid_file_valid_content_invalid_format(self):
    #     filepath = self.input_path('valid-content.base64')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.qs')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.toml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.xml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     filepath = self.input_path('valid-content.yml')
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)

    # def test_from_csv_with_valid_file_invalid_content(self):
    #     filepath = self.input_path('invalid-content.csv')
    #     # static method
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(filepath)
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(filepath, format='csv')

    def test_from_csv_with_invalid_file(self):
        filepath = self.input_path('invalid-file.csv')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_csv(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='csv')

    def test_from_csv_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.csv'
        # static method
        d = IODict.from_csv(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='csv')
        self.assertTrue(isinstance(d, dict))

    # def test_from_csv_with_valid_url_invalid_content(self):
    #     url = 'https://github.com/fabiocaccamo/python-benedict'
    #     # static method
    #     with self.assertRaises(ValueError):
    #         IODict.from_csv(url)
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(url, format='csv')

    def test_from_csv_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_csv(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='csv')

    def test_to_csv(self):
        d = IODict({
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        s = d.to_csv()
        r = """age,height,id,name,weight
20,62,1,Alice,120.6
21,74,2,Freddie,190.6
17,68,3,Bob,120.0
32,75,4,François,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_columns(self):
        d = IODict({
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        s = d.to_csv(key='values', columns=['id', 'name', 'family_name', 'age', 'height', 'gender', 'weight'])
        r = """id,name,family_name,age,height,gender,weight
1,Alice,,20,62,,120.6
2,Freddie,,21,74,,190.6
3,Bob,,17,68,,120.0
4,François,,32,75,,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_delimiter_and_quotes(self):
        d = IODict({
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        s = d.to_csv(columns=['id', 'name', 'age', 'height', 'weight'], delimiter=";", quote=True)
        r = """"id";"name";"age";"height";"weight"
"1";"Alice";"20";"62";"120.6"
"2";"Freddie";"21";"74";"190.6"
"3";"Bob";"17";"68";"120.0"
"4";"François";"32";"75";"110.05"
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_key_valid(self):
        d = IODict({
            'results': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        s = d.to_csv('results', columns=['id', 'name', 'age', 'height', 'weight'])
        r = """id,name,age,height,weight
1,Alice,20,62,120.6
2,Freddie,21,74,190.6
3,Bob,17,68,120.0
4,François,32,75,110.05
"""
        self.assertEqual(s, r)

    def test_to_csv_with_custom_key_invalid(self):
        d = IODict({
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        with self.assertRaises(KeyError):
            s = d.to_csv('invalid_values', columns=['id', 'name', 'age', 'height', 'weight'])

    def test_to_csv_file(self):
        d = IODict({
            'values': [
                { 'id':'1', 'name':'Alice', 'age':'20', 'height':'62', 'weight':'120.6', },
                { 'id':'2', 'name':'Freddie', 'age':'21', 'height':'74', 'weight':'190.6', },
                { 'id':'3', 'name':'Bob', 'age':'17', 'height':'68', 'weight':'120.0', },
                { 'id':'4', 'name':'François', 'age':'32', 'height':'75', 'weight':'110.05', },
            ],
        })
        filepath = self.output_path('test_to_csv_file.csv')
        d.to_csv(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_csv(filepath))

# JSON

    def test_from_json_with_valid_data(self):
        j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })
        # constructor
        d = IODict(j, format='json')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    def test_from_json_with_valid_data_list(self):
        j = '[0,1,2,3,4,5]'
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'values': [0, 1, 2, 3, 4, 5] })
        # constructor
        d = IODict(j, format='json')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'values': [0, 1, 2, 3, 4, 5] })

    # def test_from_json_with_valid_data_and_trailing_whitespace(self):
    #     j = '{"a": 1, "b": 2, "c": 3}\n\r\t\n'
    #     # static method
    #     d = IODict.from_json(j)
    #     self.assertTrue(isinstance(d, dict))
    #     self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    # def test_from_json_with_valid_data_and_trailing_null_chars(self):
    #     j = '{"a": 1, "b": 2, "c": 3}\x00\x00'
    #     # static method
    #     d = IODict.from_json(j)
    #     self.assertTrue(isinstance(d, dict))
    #     self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    # def test_from_json_with_valid_data_and_trailing_null_chars_and_whitespace(self):
    #     j = '{"a": 1, "b": 2, "c": 3}\n\x00\x00\n\t\n'
    #     # static method
    #     d = IODict.from_json(j)
    #     self.assertTrue(isinstance(d, dict))
    #     self.assertEqual(d, { 'a': 1, 'b': 2, 'c': 3, })

    def test_from_json_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format='json')

    def test_from_json_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.json')
        # static method
        d = IODict.from_json(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='json')
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.base64')
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path('valid-content.yml')
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)

    def test_from_json_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.json')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='json')

    def test_from_json_with_invalid_file(self):
        filepath = self.input_path('invalid-file.json')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='json')

    def test_from_json_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.json'
        # static method
        d = IODict.from_json(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='json')
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='json')

    def test_from_json_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='json')

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
        d.to_json(filepath=filepath, sort_keys=True)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_json(filepath))

# QUERY STRING

    def test_from_query_string_with_valid_data(self):
        s = 'ok=1&test=2&page=3&lib=python%20benedict&author=Fabio+Caccamo&author=Fabio%20Caccamo'
        r = { 'ok': '1', 'test': '2', 'page': '3', 'lib':'python benedict', 'author':'Fabio Caccamo' }
        # static method
        d = IODict.from_query_string(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format='query_string')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_query_string_with_invalid_data(self):
        s = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(s)
        # constructor
        with self.assertRaises(ValueError):
            IODict(s, format='query_string')

    def test_from_query_string_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.qs')
        # static method
        d = IODict.from_query_string(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='query_string')
        self.assertTrue(isinstance(d, dict))

    def test_from_query_string_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.base64')
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path('valid-content.json')
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path('valid-content.yml')
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)

    def test_from_query_string_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.qs')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='query_string')

    def test_from_query_string_with_invalid_file(self):
        filepath = self.input_path('invalid-file.qs')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='query_string')

    def test_from_query_string_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.qs'
        # static method
        d = IODict.from_query_string(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='query_string')
        self.assertTrue(isinstance(d, dict))

    def test_from_query_string_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='query_string')

    def test_from_query_string_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='query_string')

    def test_to_query_string(self):
        data = { 'ok': '1', 'test': '2', 'page': '3', 'lib':'python benedict', 'author':'Fabio Caccamo' }
        d = IODict({ 'ok': '1', 'test': '2', 'page': '3', 'lib':'python benedict', 'author':'Fabio Caccamo' })
        s = d.to_query_string()
        self.assertEqual(d, IODict.from_query_string(s))

    def test_to_query_string_file(self):
        d = IODict({ 'ok': '1', 'test': '2', 'page': '3', 'lib':'python benedict', 'author':'Fabio Caccamo' })
        filepath = self.output_path('test_to_query_string_file.qs')
        d.to_query_string(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_query_string(filepath))

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
        d = IODict(j, format='toml')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

    def test_from_toml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_toml(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format='toml')

    def test_from_toml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.toml')
        # static method
        d = IODict.from_toml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='toml')
        self.assertTrue(isinstance(d, dict))

    def test_from_toml_with_valid_file_valid_content_invalid_format(self):
        # filepath = self.input_path('valid-content.base64')
        # with self.assertRaises(ValueError):
        #     d = IODict.from_toml(filepath)
        filepath = self.input_path('valid-content.json')
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)
        filepath = self.input_path('valid-content.yml')
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)

    def test_from_toml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.toml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='toml')

    def test_from_toml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.toml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_toml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='toml')

    def test_from_toml_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.toml'
        # static method
        d = IODict.from_toml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='toml')
        self.assertTrue(isinstance(d, dict))

    def test_from_toml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_toml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='toml')

    def test_from_toml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_toml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='toml')

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
        d.to_toml(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_toml(filepath))

# XML

    def test_from_xml_with_valid_data(self):
        j = """
<?xml version="1.0" ?>
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
        d = IODict(j, format='xml')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d.get('root'), { 'a':'1', 'b':{ 'c':'3', 'd':'4' },})

    def test_from_xml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format='xml')

    def test_from_xml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.xml')
        # static method
        d = IODict.from_xml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='xml')
        self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.base64')
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path('valid-content.json')
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path('valid-content.yml')
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)

    def test_from_xml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.xml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='xml')

    def test_from_xml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.xml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='xml')

    def test_from_xml_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.xml'
        # static method
        d = IODict.from_xml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='xml')
        self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='xml')

    def test_from_xml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='xml')

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
        d.to_xml(filepath=filepath)
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
        d = IODict(j, format='yaml')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, { 'a':1, 'b':{ 'c':3, 'd':4 },})

    def test_from_yaml_with_invalid_data(self):
        j = 'Lorem ipsum est in ea occaecat nisi officia.'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format='yaml')

    def test_from_yaml_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.yml')
        # static method
        d = IODict.from_yaml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format='yaml')
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.base64')
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # filepath = self.input_path('valid-content.json')
        # with self.assertRaises(ValueError):
        #    IODict.from_yaml(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)

    def test_from_yaml_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.yml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='yaml')

    def test_from_yaml_with_invalid_file(self):
        filepath = self.input_path('invalid-file.yml')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='yaml')

    def test_from_yaml_with_valid_url_valid_content(self):
        url = 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/input/valid-content.yml'
        # static method
        d = IODict.from_yaml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='yaml')
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='yaml')

    def test_from_yaml_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='yaml')

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
        d.to_yaml(filepath=filepath)
        self.assertTrue(d, os.path.isfile(filepath))
        self.assertEqual(d, IODict.from_yaml(filepath))
