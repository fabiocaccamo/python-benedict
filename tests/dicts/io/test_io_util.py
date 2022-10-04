# -*- coding: utf-8 -*-

from benedict.dicts.io import io_util

import unittest


class io_util_test_case(unittest.TestCase):
    """
    This class describes an i/o utility test case.
    """

    def test_decode(self):
        # TODO
        pass

    def test_autodetect_format_by_data(self):
        s = '{"a": 1, "b": 2, "c": 3}'
        self.assertEqual(io_util.autodetect_format(s), None)

    def test_autodetect_format_by_path(self):
        s = "path-to/data.xml"
        self.assertEqual(io_util.autodetect_format(s), "xml")

    def test_autodetect_format_by_path_with_unsupported_format(self):
        s = "path-to/data.jpg"
        self.assertEqual(io_util.autodetect_format(s), None)

    def test_autodetect_format_by_url(self):
        s = "https://github.com/fabiocaccamo/python-benedict.xml"
        self.assertEqual(io_util.autodetect_format(s), "xml")

    def test_autodetect_format_by_url_with_unsupported_format(self):
        s = "https://github.com/fabiocaccamo/python-benedict.jpg"
        self.assertEqual(io_util.autodetect_format(s), None)

    def test_decode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.decode("", format="xxx")

    def test_encode(self):
        # TODO
        pass

    def test_encode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.encode({}, format="xxx")

    def test_is_data(self):
        # TODO
        pass

    def test_is_filepath(self):
        path = "my-folder/my-file.json"
        self.assertTrue(io_util.is_filepath(path))

    def test_is_s3_filepath(self):
        path = "s3://my-folder/my-file.json"
        self.assertTrue(io_util.is_s3_filepath(path))

    def test_is_url(self):
        path = "https://my-site.com/my-folder/my-file.json"
        self.assertTrue(io_util.is_url(path))

    def test_read_content(self):
        # TODO
        pass

    def test_read_file(self):
        # TODO
        pass

    def test_read_file_from_s3(self):
        # TODO:
        content = io_util.read_file_from_s3("s3://my-bucket/my-file.txt", anon=True)
        # print(content)
        self.assertEqual(content, None)
        pass

    def test_read_url(self):
        # TODO
        pass

    def test_write_file_dir(self):
        # TODO
        pass

    def test_write_file(self):
        # TODO
        pass

    def test_write_file_to_s3(self):
        io_util.write_file_to_s3("s3://my-bucket/my-file.txt", "ok", anon=True)
