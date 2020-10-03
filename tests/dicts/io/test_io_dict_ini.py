# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case

TARGET_DICT = {
    "section_a": {
        "b": 1,
        "c": "helloworld"
    },
    "section_b": {
        "c": 2.5,
        "f": True,
        "g": True,
        "h": False,
        "j": False
    }
}

INI_STR = """
        [section_a]
        b: 1
        c: helloworld
        [section_b]
        c: 2.5
        f: True
        g: true
        h: false
        j: False
        """

INVALID_INI_STR = """
    {test}
    abc = def 
    """


class io_dict_ini_test_case(io_dict_test_case):

    def test_from_ini_with_valid_data(self):
        # static method
        d = IODict.from_ini(INI_STR)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, TARGET_DICT)
        # constructor
        d = IODict(INI_STR, format='ini')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, TARGET_DICT)

    def test_from_ini_with_invalid_data(self):
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(INVALID_INI_STR)
        # constructor
        with self.assertRaises(ValueError):
            IODict(INVALID_INI_STR, format='ini')

    def test_from_ini_with_valid_file_valid_content(self):
        filepath = self.input_path('valid-content.ini')
        # static method
        d = IODict.from_ini(filepath)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, TARGET_DICT)
        # constructor
        d = IODict(filepath, format='ini')
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, TARGET_DICT)
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, TARGET_DICT)

    def test_from_ini_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path('valid-content.base64')
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path('valid-content.json')
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path('valid-content.qs')
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path('valid-content.toml')
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        filepath = self.input_path('valid-content.xml')
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)

    def test_from_ini_with_valid_file_invalid_content(self):
        filepath = self.input_path('invalid-content.ini')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='ini')

    def test_from_ini_with_invalid_file(self):
        filepath = self.input_path('invalid-file.ini')
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format='ini')

    def test_from_ini_with_valid_url_valid_content(self):
        url = self.input_url('valid-content.ini')
        # static method
        d = IODict.from_ini(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format='ini')
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_ini_with_valid_url_invalid_content(self):
        url = 'https://github.com/fabiocaccamo/python-benedict'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='ini')

    def test_from_ini_with_invalid_url(self):
        url = 'https://github.com/fabiocaccamo/python-benedict-invalid'
        # static method
        with self.assertRaises(ValueError):
            IODict.from_ini(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format='ini')

    def test_to_ini(self):
        d = IODict(TARGET_DICT)
        s = d.to_ini()
        self.assertEqual(d, IODict.from_ini(s))

    def test_to_ini_file(self):
        d = IODict(TARGET_DICT)
        filepath = self.output_path('test_to_ini_file.ini')
        d.to_ini(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_ini(filepath))
