import base64
import json
import unittest

from benedict import benedict
from benedict.serializers.base64 import Base64CoreSerializer


class base64_serializer_test_case(unittest.TestCase):
    """
    This class describes a base64 serializer test case.
    """

    def test_decode_base64(self) -> None:
        serializer = Base64CoreSerializer()
        text = "hello world"
        for encoding in ("utf-8", "utf-16", "cp037"):
            with self.subTest(encoding=encoding):
                encoded = base64.b64encode(text.encode(encoding)).decode("ascii")
                self.assertEqual(serializer.decode(encoded, encoding=encoding), text)

    def test_encode_base64(self) -> None:
        serializer = Base64CoreSerializer()
        text = "hello world"
        for encoding in ("utf-8", "utf-16", "cp037"):
            with self.subTest(encoding=encoding):
                expected = base64.b64encode(text.encode(encoding)).decode("ascii")
                self.assertEqual(serializer.encode(text, encoding=encoding), expected)

    def test_binary_roundtrip_without_encoding(self) -> None:
        serializer = Base64CoreSerializer()
        payload = b"\xff\x00\x81"
        encoded = serializer.encode(payload, encoding=None)
        self.assertEqual(encoded, base64.b64encode(payload).decode("ascii"))
        self.assertEqual(serializer.decode(encoded, encoding=None), payload)

    def test_dict_roundtrip_with_non_ascii_payload_encoding(self) -> None:
        payload = benedict({"hello": "world"})
        for encoding in ("utf-16", "cp037"):
            with self.subTest(encoding=encoding):
                encoded = payload.to_base64(encoding=encoding)
                self.assertEqual(
                    base64.b64decode(encoded).decode(encoding), json.dumps(payload)
                )
                self.assertEqual(
                    benedict.from_base64(encoded, encoding=encoding), payload
                )
