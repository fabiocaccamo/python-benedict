from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_yaml_test_case(io_dict_test_case):
    """
    This class describes an IODict / yaml test case.
    """

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
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )
        # constructor
        d = IODict(j, format="yaml")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(
            d,
            {
                "a": 1,
                "b": {
                    "c": 3,
                    "d": 4,
                },
            },
        )

    def test_from_yaml_with_invalid_data(self):
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="yaml")

    def test_from_yaml_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.yml")
        # static method
        d = IODict.from_yaml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="yaml")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # filepath = self.input_path('valid-content.json')
        # with self.assertRaises(ValueError):
        #    IODict.from_yaml(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)

    def test_from_yaml_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.yml")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="yaml")

    def test_from_yaml_with_invalid_file(self):
        filepath = self.input_path("invalid-file.yml")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="yaml")

    def test_from_yaml_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.yml")
        # static method
        d = IODict.from_yaml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="yaml")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_yaml_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="yaml")

    def test_from_yaml_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_yaml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="yaml")

    def test_to_yaml(self):
        d = IODict(
            {
                "x": 7,
                "y": 8,
                "z": 9,
                "a": 1,
                "b": 2,
                "c": 3,
            }
        )
        s = d.to_yaml()
        self.assertEqual(d, IODict.from_yaml(s))

    def test_to_yaml_file(self):
        d = IODict(
            {
                "x": 7,
                "y": 8,
                "z": 9,
                "a": 1,
                "b": 2,
                "c": 3,
            }
        )
        filepath = self.output_path("test_to_yaml_file.yml")
        d.to_yaml(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_yaml(filepath))
