from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_base64_test_case(io_dict_test_case):
    """
    This class describes an IODict / base64 test case.
    """

    def test_from_base64_with_valid_data(self):
        j = "eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9"
        # j = '{"a": 1, "b": 2, "c": 3}'
        # static method
        d = IODict.from_base64(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3})
        # constructor
        d = IODict(j, format="base64")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3})
        # constructor with subformat
        d = IODict(j, format="base64", subformat="json")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3})

    def test_from_base64_with_valid_data_without_padding(self):
        j = "eyJhIjogMSwgImIiOiAyLCAiYyI6IDMsICJkIjogNH0"
        # eyJhIjogMSwgImIiOiAyLCAiYyI6IDMsICJkIjogNH0=
        # j = '{"a": 1, "b": 2, "c": 3, "d": 4}'
        # static method
        d = IODict.from_base64(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3, "d": 4})
        # constructor
        d = IODict(j, format="base64")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, {"a": 1, "b": 2, "c": 3, "d": 4})

    def test_from_base64_with_invalid_data(self):
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="base64")

    def test_from_base64_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.base64")
        # static method
        d = IODict.from_base64(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="base64")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_base64_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)

    def test_from_base64_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.base64")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="base64")

    def test_from_base64_with_invalid_file(self):
        filepath = self.input_path("invalid-file.base64")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="base64")

    def test_from_base64_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.base64")
        # static method
        d = IODict.from_base64(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="base64")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_base64_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="base64")

    def test_from_base64_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_base64(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="base64")

    def test_to_base64(self):
        d = IODict({"a": 1, "b": 2, "c": 3})
        s = d.to_base64(sort_keys=True)
        self.assertEqual(s, "eyJhIjogMSwgImIiOiAyLCAiYyI6IDN9")

    def test_to_base64_file(self):
        d = IODict({"a": 1, "b": 2, "c": 3})
        filepath = self.output_path("test_to_base64_file.base64")
        d.to_base64(filepath=filepath, sort_keys=True)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_base64(filepath))
