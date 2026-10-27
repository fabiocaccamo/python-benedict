from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from benedict import benedict


class io_dict_s3_test_case(unittest.TestCase):
    def test_to_json_s3_client_and_serializer_options(self) -> None:
        for options in (
            {},
            {"s3_options": None},
            {"s3_options": {}},
            {"s3_options": {"region_name": "us-east-1"}},
        ):
            with self.subTest(options=options):
                data = {"z": 1, "a": "example"}
                expected = json.dumps(data, indent=2, sort_keys=True)
                with tempfile.TemporaryDirectory() as directory:
                    temporary_path = os.path.join(directory, "output.json")

                    def upload(
                        filepath: str,
                        bucket: str,
                        key: str,
                        expected_path: str = temporary_path,
                        expected_content: str = expected,
                    ) -> None:
                        self.assertEqual(filepath, expected_path)
                        self.assertEqual(bucket, "test-bucket")
                        self.assertEqual(key, "folder/output.json")
                        self.assertEqual(Path(filepath).read_text(), expected_content)

                    with (
                        patch(
                            "benedict.dicts.io.io_util.tempfile.gettempdir",
                            return_value=directory,
                        ),
                        patch("benedict.dicts.io.io_util.boto3.client") as client,
                    ):
                        client.return_value.upload_file.side_effect = upload
                        result = benedict(data).to_json(
                            filepath="s3://test-bucket/folder/output.json",
                            indent=2,
                            sort_keys=True,
                            **options,
                        )
                        self.assertEqual(result, expected)
                        client.assert_called_once_with(
                            "s3", **(options.get("s3_options") or {})
                        )
                        client.return_value.upload_file.assert_called_once()
                        client.return_value.close.assert_called_once_with()
                    self.assertFalse(Path(temporary_path).exists())

    def test_output_formats_accept_s3_options(self) -> None:
        data = benedict({"root": {"name": "example", "count": 3}})
        options: dict[str, Any] = {"region_name": "us-east-1"}
        for method in (
            "to_base64",
            "to_ini",
            "to_json",
            "to_pickle",
            "to_plist",
            "to_query_string",
            "to_toml",
            "to_xml",
            "to_yaml",
        ):
            with self.subTest(method=method):
                encode = getattr(data, method)
                expected = encode()
                with patch("benedict.dicts.io.io_util.write_content") as write:
                    actual = encode(
                        filepath="s3://test-bucket/output",
                        s3_options=options,
                    )
                    self.assertEqual(actual, expected)
                    write.assert_called_once()
                    self.assertEqual(
                        write.call_args.args, ("s3://test-bucket/output", expected)
                    )
                    self.assertEqual(write.call_args.kwargs["s3_options"], options)
                    self.assertEqual(options, {"region_name": "us-east-1"})
