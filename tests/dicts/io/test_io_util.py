import tempfile
import unittest
from unittest.mock import MagicMock, patch

import fsutil
from decouple import config

from benedict.dicts.io import io_util
from benedict.dicts.io.io_util import parse_s3_url
from benedict.exceptions import ExtrasRequireModuleNotFoundError


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

    def test_is_s3_with_txt_document(self):
        path = "s3://my-folder/my-file.txt"
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

    def test_parse_s3_url_valid(self):
        url = "s3://my-bucket/path/to/key"
        result = io_util.parse_s3_url(url)
        expected_result = {
            "url": url,
            "bucket": "my-bucket",
            "key": "path/to/key",
        }
        self.assertEqual(result, expected_result)

    def test_parse_s3_url_with_query(self):
        url = "s3://my-bucket/path/to/key?versionId=123"
        result = io_util.parse_s3_url(url)
        expected_result = {
            "url": url,
            "bucket": "my-bucket",
            "key": "path/to/key?versionId=123",
        }
        self.assertEqual(result, expected_result)

    def test_parse_s3_url_with_multiple_query_parameters(self):
        url = "s3://my-bucket/path/to/key?versionId=123&foo=bar"
        result = io_util.parse_s3_url(url)
        expected_result = {
            "url": url,
            "bucket": "my-bucket",
            "key": "path/to/key?versionId=123&foo=bar",
        }
        self.assertEqual(result, expected_result)

    def test_parse_s3_url_with_special_characters(self):
        url = "s3://my-bucket/path/to/key with spaces?foo=bar&baz=qux"
        result = io_util.parse_s3_url(url)
        expected_result = {
            "url": url,
            "bucket": "my-bucket",
            "key": "path/to/key with spaces?foo=bar&baz=qux",
        }
        self.assertEqual(result, expected_result)

    @patch("benedict.dicts.io.io_util.s3_installed", False)
    def test_read_content_from_s3_with_s3_extra_not_installed(self):
        s3_options = {
            "aws_access_key_id": "",
            "aws_secret_access_key": "",
        }
        s3_url = "s3://my-bucket/my-key.txt"
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            io_util.read_content_from_s3(s3_url, s3_options)

    @patch("benedict.dicts.io.io_util.s3_installed", True)
    @patch("benedict.dicts.io.io_util.boto3.client")
    @patch("benedict.dicts.io.io_util.read_content_from_file")
    def test_read_content_from_s3(self, mock_read_content_from_file, mock_boto3_client):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        s3_url = "s3://my-bucket/my-key.txt"
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_read_content_from_file.return_value = "s3 content"

        content = io_util.read_content_from_s3(s3_url, s3_options, format="txt")

        mock_boto3_client.assert_called_with("s3", **s3_options)
        s3_url_parsed = parse_s3_url(s3_url)
        temporary_filepath = fsutil.join_path(
            tempfile.gettempdir(), fsutil.get_filename(s3_url_parsed["key"])
        )
        mock_s3.download_file.assert_called_with(
            s3_url_parsed["bucket"], s3_url_parsed["key"], temporary_filepath
        )
        mock_s3.close.assert_called()
        mock_read_content_from_file.assert_called_with(temporary_filepath, "txt")
        self.assertEqual(content, "s3 content")

    @patch("benedict.dicts.io.io_util.s3_installed", True)
    @patch("benedict.dicts.io.io_util.boto3.client")
    @patch("benedict.dicts.io.io_util.fsutil.remove_file")
    @patch("benedict.dicts.io.io_util.fsutil.write_file")
    def test_write_content_to_s3(
        self, mock_write_file, mock_remove_file, mock_boto3_client
    ):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        s3_url = "s3://my-bucket/my-key.txt"
        content = "s3 content"

        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3
        mock_write_file.return_value = None
        mock_remove_file.return_value = None

        io_util.write_content_to_s3(s3_url, content, s3_options=s3_options)

        mock_boto3_client.assert_called_with("s3", **s3_options)
        s3_url_parsed = parse_s3_url(s3_url)
        temporary_filepath = fsutil.join_path(
            tempfile.gettempdir(), fsutil.get_filename(s3_url_parsed["key"])
        )
        mock_write_file.assert_called_with(temporary_filepath, content)
        mock_s3.upload_file.assert_called_with(
            temporary_filepath, s3_url_parsed["bucket"], s3_url_parsed["key"]
        )
        mock_s3.close.assert_called()
        mock_remove_file.assert_called_with(temporary_filepath)

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

    def test_write_and_read_content_s3_with_s3_url_autodetection(self):
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
        io_util.write_content(filepath, "ok", s3_options=s3_options)
        content = io_util.read_content(filepath, options={"s3_options": s3_options})
        self.assertEqual(content, "ok")

    @patch("benedict.dicts.io.io_util.s3_installed", False)
    def test_write_and_read_content_s3_with_s3_extra_not_installed(self):
        aws_access_key_id = config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY", default=None)
        if not all([aws_access_key_id, aws_secret_access_key]):
            # skip s3 on GH CI
            return
        s3_options = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }
        filepath = "s3://python-benedict/test-extras-require-s3.txt"
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            io_util.write_content_to_s3(filepath, "ok", s3_options=s3_options)
