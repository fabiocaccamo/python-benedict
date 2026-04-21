import unittest

from benedict import benedict
from benedict.dicts.io import IODict
from benedict.serializers import TOMLSerializer


class toml_serializer_test_case(unittest.TestCase):
    """
    This class describes a toml serializer test case.

    Regression coverage for issue #439 — the uiri/toml encoder crashes
    on certain strings. These tests pin the encode path to a library
    that handles them correctly and guard against regression.
    """

    def test_encode_ansi_control_character(self):
        """Scenario 1 — falsification clause #1.

        `benedict({"color": "\033[31m"}).to_toml()` must not raise. On
        baseline (uiri/toml) this raises IndexError in the encoder.
        """
        payload = {"color": "\033[31m"}
        encoded = benedict(payload).to_toml()
        self.assertIsInstance(encoded, str)
        self.assertGreater(len(encoded), 0)
        # Round-trip: decoded value must equal the original string.
        decoded = IODict.from_toml(encoded)
        self.assertEqual(decoded["color"], "\033[31m")

    def test_encode_issue_439_literal_examples(self):
        """Scenario 2 — regression guard for issue #439's cited examples.

        These pass on baseline (literal backslashes, not control chars).
        Kept so the encoder swap does not silently regress them.
        """
        payload = {
            "reset": "\\033\\[00;00m",
            "lightblue": "\\033\\[01;30m",
        }
        encoded = benedict(payload).to_toml()
        self.assertIsInstance(encoded, str)
        decoded = IODict.from_toml(encoded)
        self.assertEqual(decoded["reset"], "\\033\\[00;00m")
        self.assertEqual(decoded["lightblue"], "\\033\\[01;30m")

    def test_roundtrip_control_chars_and_unicode(self):
        """Scenario 4 — round-trip integrity across tricky values."""
        payload = {
            "ansi_red": "\033[31m",
            "ansi_reset": "\033[0m",
            "bell": "\x07",
            "tab_and_newline": "a\tb\nc",
            "unicode_emoji": "benedict 🎩",
            "backslash": "path\\to\\file",
            "quotes": 'he said "hi"',
        }
        encoded = benedict(payload).to_toml()
        decoded = IODict.from_toml(encoded)
        for key, value in payload.items():
            self.assertEqual(decoded[key], value, f"round-trip mismatch for {key!r}")

    def test_encode_nested_dict(self):
        """Structural coverage — nested dicts still encode correctly."""
        payload = {
            "section": {
                "key": "value",
                "control": "\033[31m",
            }
        }
        encoded = benedict(payload).to_toml()
        decoded = IODict.from_toml(encoded)
        self.assertEqual(decoded["section"]["key"], "value")
        self.assertEqual(decoded["section"]["control"], "\033[31m")

    def test_serializer_decode_roundtrip(self):
        """Direct serializer-level round-trip (bypasses IODict convenience layer)."""
        serializer = TOMLSerializer()
        payload = {"color": "\033[31m", "count": 42}
        encoded = serializer.encode(payload)
        decoded = serializer.decode(encoded)
        self.assertEqual(decoded, payload)
