from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_xml_test_case(io_dict_test_case):
    """
    This class describes an IODict / xml test case.
    """

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
        self.assertEqual(
            d.get("root"),
            {
                "a": "1",
                "b": {"c": "3", "d": "4"},
            },
        )
        # constructor
        d = IODict(j, format="xml")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(
            d.get("root"),
            {
                "a": "1",
                "b": {"c": "3", "d": "4"},
            },
        )

    def test_from_xml_with_invalid_data(self):
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="xml")

    def test_from_xml_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.xml")
        # static method
        d = IODict.from_xml(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="xml")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_file_valid_content_invalid_format(self):
        filepath = self.input_path("valid-content.base64")
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)

    def test_from_xml_with_valid_file_invalid_content(self):
        filepath = self.input_path("invalid-content.xml")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="xml")

    def test_from_xml_with_invalid_file(self):
        filepath = self.input_path("invalid-file.xml")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="xml")

    def test_from_xml_with_valid_url_valid_content(self):
        url = self.input_url("valid-content.xml")
        # static method
        d = IODict.from_xml(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="xml")
        self.assertTrue(isinstance(d, dict))
        # constructor with format autodetection
        d = IODict(url)
        self.assertTrue(isinstance(d, dict))

    def test_from_xml_with_valid_url_invalid_content(self):
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="xml")

    def test_from_xml_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xml(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="xml")

    def test_to_xml(self):
        d = IODict(
            {
                "root": {
                    "x": "7",
                    "y": "8",
                    "z": "9",
                    "a": "1",
                    "b": "2",
                    "c": "3",
                },
            }
        )
        s = d.to_xml()
        self.assertEqual(d, IODict.from_xml(s))

    def test_to_xml_file(self):
        d = IODict(
            {
                "root": {
                    "x": "7",
                    "y": "8",
                    "z": "9",
                    "a": "1",
                    "b": "2",
                    "c": "3",
                },
            }
        )
        filepath = self.output_path("test_to_xml_file.xml")
        d.to_xml(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_xml(filepath))
