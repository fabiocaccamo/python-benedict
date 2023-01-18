from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_query_string_test_case(io_dict_test_case):
    """
    This class describes an IODict / query-string test case.
    """

    def test_from_query_string_with_valid_data(self):
        s = "ok=1&test=2&page=3&lib=python%20benedict&author=Fabio+Caccamo&author=Fabio%20Caccamo"
        r = {
            "ok": "1",
            "test": "2",
            "page": "3",
            "lib": "python benedict",
            "author": "Fabio Caccamo",
        }
        # static method
        d = IODict.from_query_string(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format="query_string")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_query_string_with_invalid_data(self):
        s = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(s)
        # constructor
        with self.assertRaises(ValueError):
            IODict(s, format="query_string")

    def test_from_query_string_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.qs")
        # static method
        d = IODict.from_query_string(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="query_string")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_query_string_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)

    def test_from_query_string_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.qs")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="query_string")

    def test_from_query_string_with_invalid_file(self):
        filepath = self.input_path("invalid-file.qs")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="query_string")

    def test_from_query_string_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.qs")
        # static method
        d = IODict.from_query_string(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="query_string")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_query_string_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="query_string")

    def test_from_query_string_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_query_string(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="query_string")

    def test_to_query_string(self):
        data = {
            "ok": "1",
            "test": "2",
            "page": "3",
            "lib": "python benedict",
            "author": "Fabio Caccamo",
        }
        d = IODict(
            {
                "ok": "1",
                "test": "2",
                "page": "3",
                "lib": "python benedict",
                "author": "Fabio Caccamo",
            }
        )
        s = d.to_query_string()
        self.assertEqual(d, IODict.from_query_string(s))

    def test_to_query_string_file(self):
        d = IODict(
            {
                "ok": "1",
                "test": "2",
                "page": "3",
                "lib": "python benedict",
                "author": "Fabio Caccamo",
            }
        )
        filepath = self.output_path("test_to_query_string_file.qs")
        d.to_query_string(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_query_string(filepath))
