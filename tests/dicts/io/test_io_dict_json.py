from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_json_test_case(io_dict_test_case):
    """
    This class describes an IODict / json test case.
    """

    def test_from_json_with_valid_data(self):
        j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3})
        # constructor
        d = IODict(j, format="json")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3})

    def test_from_json_with_valid_data_empty(self):
        j = "{}"
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {})
        # constructor
        d = IODict(j, format="json")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {})

    def test_from_json_with_valid_data_list(self):
        j = "[0,1,2,3,4,5]"
        # static method
        d = IODict.from_json(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"values": [0, 1, 2, 3, 4, 5]})
        # constructor
        d = IODict(j, format="json")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"values": [0, 1, 2, 3, 4, 5]})

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
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="json")

    def test_from_json_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.json")
        # static method
        d = IODict.from_json(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="json")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_file_valid_content_but_unexpected_extension(self):
        filepath = self.input_path("valid-content.json.txt")
        # static method
        d = IODict.from_json(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="json")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)

    def test_from_json_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.json")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="json")

    def test_from_json_with_invalid_file(self):
        filepath = self.input_path("invalid-file.json")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="json")

    def test_from_json_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.json")
        # static method
        d = IODict.from_json(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="json")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_json_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="json")

    def test_from_json_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_json(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="json")

    def test_to_json(self):
        d = IODict({"x": 7, "y": 8, "z": 9, "a": 1, "b": 2, "c": 3})
        s = d.to_json(sort_keys=True)
        self.assertEqual(s, '{"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9}')

    def test_to_json_file(self):
        d = IODict({"x": 7, "y": 8, "z": 9, "a": 1, "b": 2, "c": 3})
        filepath = self.output_path("test_to_json_file.json")
        d.to_json(filepath=filepath, sort_keys=True)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_json(filepath))
