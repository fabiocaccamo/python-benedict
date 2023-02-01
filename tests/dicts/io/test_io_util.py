import unittest

from decouple import config

from benedict.dicts.io import io_util


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

    def test_is_s3(self):
        path = "s3://my-folder/my-file.json"
        self.assertTrue(io_util.is_s3(path))

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
        pass

    def test_read_url(self):
        # TODO
        pass

    def test_write_file(self):
        # TODO
        pass

    def test_write_file_to_s3(self):
        # TODO:
        # io_util.write_file_to_s3("s3://test-bucket/my-file.txt", "ok", anon=True)
        pass

    def test_write_and_read_content_s3(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        if not all([aws_access_key_id, aws_secret_access_key]):
            # skip s3 on GH CI
            return
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        filepath = "s3://python-benedict/test-io.txt"
        io_util.write_content_to_s3(filepath, "ok", s3_options=s3_options)
        content = io_util.read_content_from_s3(filepath, s3_options=s3_options)
        self.assertEqual(content, "ok")
