import unittest
from unittest.mock import MagicMock, patch

from benedict.dicts.io import io_util


class s3_cleanup_test_case(unittest.TestCase):
    def test_download_failure_closes_client(self) -> None:
        client = MagicMock()
        client.download_file.side_effect = RuntimeError("download failed")
        with patch.object(io_util.boto3, "client", return_value=client):
            with self.assertRaisesRegex(RuntimeError, "download failed"):
                io_util.read_content_from_s3("s3://bucket/data.json", {})
        client.close.assert_called_once_with()

    def test_upload_failure_closes_client_and_removes_temp_file(self) -> None:
        client = MagicMock()
        client.upload_file.side_effect = RuntimeError("upload failed")
        with (
            patch.object(io_util.boto3, "client", return_value=client),
            patch.object(io_util.fsutil, "write_file") as write,
            patch.object(io_util.fsutil, "remove_file") as remove,
        ):
            with self.assertRaisesRegex(RuntimeError, "upload failed"):
                io_util.write_content_to_s3("s3://bucket/data.json", "{}", {})
        client.close.assert_called_once_with()
        remove.assert_called_once_with(write.call_args.args[0])

    def test_client_setup_failure_removes_upload_temp_file(self) -> None:
        with (
            patch.object(
                io_util.boto3, "client", side_effect=RuntimeError("setup failed")
            ),
            patch.object(io_util.fsutil, "write_file") as write,
            patch.object(io_util.fsutil, "remove_file") as remove,
        ):
            with self.assertRaisesRegex(RuntimeError, "setup failed"):
                io_util.write_content_to_s3("s3://bucket/data.json", "{}", {})
        remove.assert_called_once_with(write.call_args.args[0])

    def test_client_close_failure_still_removes_upload_temp_file(self) -> None:
        client = MagicMock()
        client.close.side_effect = RuntimeError("close failed")
        with (
            patch.object(io_util.boto3, "client", return_value=client),
            patch.object(io_util.fsutil, "write_file") as write,
            patch.object(io_util.fsutil, "remove_file") as remove,
        ):
            with self.assertRaisesRegex(RuntimeError, "close failed"):
                io_util.write_content_to_s3("s3://bucket/data.json", "{}", {})
        remove.assert_called_once_with(write.call_args.args[0])
