# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_xls_test_case(io_dict_test_case):
    """
    This class describes an IODict / xls test case.
    """

    def test_from_xls_with_valid_file_valid_content(self):
        filepath = self.input_path("valid-content.xls")
        # static method
        d = IODict.from_xls(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="xls")
        self.assertTrue(isinstance(d, dict))

    def test_from_xls_with_invalid_file(self):
        filepath = self.input_path("invalid-file.xls")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xls(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="xls")

    # def test_from_xls_with_valid_url_invalid_content(self):
    #     url = 'https://github.com/fabiocaccamo/python-benedict'
    #     # static method
    #     with self.assertRaises(ValueError):
    #         IODict.from_xls(url)
    #     # constructor
    #     with self.assertRaises(ValueError):
    #         IODict(url, format='xls')

    def test_from_xls_with_invalid_url(self):
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_xls(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="xls")
