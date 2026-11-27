import unittest
from unittest.mock import patch

from benedict import benedict


class io_dict_s3_test_case(unittest.TestCase):
    def test_to_json_s3_client_and_serializer_options(self) -> None:
        for options in ({}, {"s3_options": {"region_name": "us-east-1"}}):
            with (
                self.subTest(options=options),
                patch("benedict.dicts.io.io_util.boto3.client") as client,
            ):
                result = benedict({"a": 1}).to_json(
                    filepath="s3://test-bucket/folder/output.json", indent=2, **options
                )
                self.assertEqual(result, '{\n  "a": 1\n}')
                client.assert_called_once_with("s3", **options.get("s3_options", {}))
                upload_args = client.return_value.upload_file.call_args.args
                self.assertEqual(upload_args[1:], ("test-bucket", "folder/output.json"))
