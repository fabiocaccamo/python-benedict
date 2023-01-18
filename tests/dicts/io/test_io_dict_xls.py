from decouple import config

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_xls_test_case(io_dict_test_case):
    """
    This class describes an IODict / xls test case.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extensions = [
            "xlsx",
            "xlsm",
            "xls",
        ]

    def test_from_xls_with_valid_file_valid_content(self):
        expected_dict = {
            "values": [
                {
                    "mon": 10,
                    "tue": 11,
                    "wed": 12,
                    "thu": 13,
                    "fri": 14,
                    "sat": 15,
                    "sun": 16,
                },
                {
                    "mon": 20,
                    "tue": 21,
                    "wed": 22,
                    "thu": 23,
                    "fri": 24,
                    "sat": 25,
                    "sun": 26,
                },
                {
                    "mon": 30,
                    "tue": 31,
                    "wed": 32,
                    "thu": 33,
                    "fri": 34,
                    "sat": 35,
                    "sun": 36,
                },
            ]
        }
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_file_valid_content"
            ):
                filepath = self.input_path(f"valid-content.{extension}")
                # static method
                d = IODict.from_xls(filepath)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor explicit format
                d = IODict(filepath, format=extension)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor implicit format
                d = IODict(filepath)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)

    def test_from_xls_with_valid_url_valid_content(self):
        expected_dict = {
            "values": [
                {
                    "mon": 10,
                    "tue": 11,
                    "wed": 12,
                    "thu": 13,
                    "fri": 14,
                    "sat": 15,
                    "sun": 16,
                },
                {
                    "mon": 20,
                    "tue": 21,
                    "wed": 22,
                    "thu": 23,
                    "fri": 24,
                    "sat": 25,
                    "sun": 26,
                },
                {
                    "mon": 30,
                    "tue": 31,
                    "wed": 32,
                    "thu": 33,
                    "fri": 34,
                    "sat": 35,
                    "sun": 36,
                },
            ]
        }
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_url_valid_content"
            ):
                # url = f"https://github.com/fabiocaccamo/python-benedict/raw/s3/tests/dicts/io/input/valid-content.{extension}"
                url = f"https://github.com/fabiocaccamo/python-benedict/raw/master/tests/dicts/io/input/valid-content.{extension}"
                # static method
                d = IODict.from_xls(url)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor explicit format
                d = IODict(url, format=extension)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor implicit format
                d = IODict(url)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)

    def test_from_xls_with_valid_s3_url_valid_content(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        if not all([aws_access_key_id, aws_secret_access_key]):
            # don't use s3 on GH CI
            return
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        expected_dict = {
            "values": [
                {
                    "mon": 10,
                    "tue": 11,
                    "wed": 12,
                    "thu": 13,
                    "fri": 14,
                    "sat": 15,
                    "sun": 16,
                },
                {
                    "mon": 20,
                    "tue": 21,
                    "wed": 22,
                    "thu": 23,
                    "fri": 24,
                    "sat": 25,
                    "sun": 26,
                },
                {
                    "mon": 30,
                    "tue": 31,
                    "wed": 32,
                    "thu": 33,
                    "fri": 34,
                    "sat": 35,
                    "sun": 36,
                },
            ]
        }
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_s3_url_valid_content"
            ):
                url = f"s3://python-benedict/valid-content.{extension}"
                # static method
                d = IODict.from_xls(url, s3_options=s3_options)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor explicit format
                d = IODict(url, format=extension, s3_options=s3_options)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)
                # constructor implicit format
                d = IODict(url, s3_options=s3_options)
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)

    def test_from_xls_with_valid_file_valid_content_custom_sheet_by_index_and_columns(
        self,
    ):
        expected_dict = {
            "values": [
                {
                    "name": "Red",
                    "hex": "#FF0000",
                },
                {
                    "name": "Green",
                    "hex": "#00FF00",
                },
                {
                    "name": "Blue",
                    "hex": "#0000FF",
                },
            ]
        }
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_file_valid_content_custom_sheet_by_index_and_columns"
            ):
                filepath = self.input_path(f"valid-content.{extension}")
                # static method
                d = IODict.from_xls(
                    filepath,
                    sheet=1,
                    columns=["name", "hex"],
                    columns_row=False,
                )
                self.assertTrue(isinstance(d, dict))
                self.assertEqual(d, expected_dict)

    def test_from_xls_with_invalid_file(self):
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_file_valid_content"
            ):
                filepath = self.input_path(f"invalid-file.{extension}")
                # static method
                with self.assertRaises(ValueError):
                    IODict.from_xls(filepath)
                # constructor explicit format
                with self.assertRaises(ValueError):
                    IODict(filepath, format=extension)
                # constructor implicit format
                with self.assertRaises(ValueError):
                    IODict(filepath)

    def test_from_xls_with_valid_url_invalid_content(self):
        for extension in self._extensions:
            with self.subTest(
                msg=f"test_from_xls_({extension})_with_valid_url_invalid_content"
            ):
                url = "https://github.com/fabiocaccamo/python-benedict"
                # static method
                with self.assertRaises(ValueError):
                    IODict.from_xls(url)
                # constructor explicit format
                with self.assertRaises(ValueError):
                    IODict(url, format=extension)
                # constructor implicit format
                with self.assertRaises(ValueError):
                    IODict(url)

    def test_from_xls_with_invalid_url(self):
        for extension in self._extensions:
            with self.subTest(msg=f"test_from_xls_({extension})_with_invalid_url"):
                url = "https://github.com/fabiocaccamo/python-benedict-invalid"
                # static method
                with self.assertRaises(ValueError):
                    IODict.from_xls(url)
                # constructor explicit format
                with self.assertRaises(ValueError):
                    IODict(url, format=extension)
                # constructor implicit format
                with self.assertRaises(ValueError):
                    IODict(url)
