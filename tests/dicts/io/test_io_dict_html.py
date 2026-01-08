from unittest.mock import patch

from benedict.dicts.io import IODict
from benedict.exceptions import ExtrasRequireModuleNotFoundError

from .test_io_dict import io_dict_test_case


class io_dict_html_test_case(io_dict_test_case):
    """
    This class describes an IODict / html test case.
    """

    def test_from_html_with_valid_file_valid_content(self) -> None:
        filepath = self.input_path("valid-content.html")
        expected_title = (
            "Fabio Caccamo - Python/Django full-stack developer - Torino, Italy"
        )
        # static method
        d = IODict.from_html(filepath)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d["html"]["head"]["title"], expected_title)
        # constructor explicit format
        d = IODict(filepath, format="html")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d["html"]["head"]["title"], expected_title)
        # constructor implicit format
        d = IODict(filepath)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d["html"]["head"]["title"], expected_title)

    @patch("benedict.serializers.html.html_installed", False)
    def test_from_html_with_valid_file_valid_content_but_xls_extra_not_installed(
        self,
    ) -> None:
        filepath = self.input_path("valid-content.html")
        # static method
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            _ = IODict.from_html(filepath)
        # constructor explicit format
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            _ = IODict(filepath, format="html")
        # constructor implicit format
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            _ = IODict(filepath)

    def test_from_html_with_valid_url_valid_content(self) -> None:
        expected_title = (
            "Fabio Caccamo - Python/Django full-stack developer - Torino, Italy"
        )
        url = "https://github.com/fabiocaccamo/python-benedict/raw/s3/tests/dicts/io/input/valid-content.html"
        # static method
        d = IODict.from_html(url)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d["html"]["head"]["title"], expected_title)
        # constructor explicit format
        d = IODict(url, format="html")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d["html"]["head"]["title"], expected_title)
        # constructor implicit format (because there is not .html extension in the url)
        with self.assertRaises(ValueError):
            _ = IODict(url)

    def test_from_html_with_invalid_file(self) -> None:
        filepath = self.input_path("invalid-file.html")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_html(filepath)
        # constructor explicit format
        with self.assertRaises(ValueError):
            IODict(filepath, format="html")
        # constructor implicit format
        with self.assertRaises(ValueError):
            IODict(filepath)

    def test_from_html_with_valid_url_invalid_content(self) -> None:
        url = "https://raw.githubusercontent.com/fabiocaccamo/python-benedict/main/README.md"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_html(url)
        # constructor explicit format
        with self.assertRaises(ValueError):
            IODict(url, format="html")
        # constructor implicit format
        with self.assertRaises(ValueError):
            IODict(url)

    def test_from_html_with_invalid_url(self) -> None:
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_html(url)
        # constructor explicit format
        with self.assertRaises(ValueError):
            IODict(url, format="html")
        # constructor implicit format
        with self.assertRaises(ValueError):
            IODict(url)

    def test_to_html(self) -> None:
        d = IODict(
            {
                "html": {
                    "head": {},
                    "body": {},
                },
            }
        )
        with self.assertRaises(NotImplementedError):
            _ = d.to_html()
