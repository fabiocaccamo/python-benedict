import unittest

# from benedict.serializers import CSVSerializer


class csv_serializer_test_case(unittest.TestCase):
    """
    This class describes a csv serializer test case.
    """

    def test_decode_csv(self) -> None:
        # TODO
        pass

    def test_decode_csv_newlines(self) -> None:
        from benedict.serializers import CSVSerializer

        serializer = CSVSerializer()
        for newline in ("\r", "\n", "\r\n"):
            with self.subTest(newline=newline):
                text = f'name,note{newline}Alice,"first\r\nsecond"{newline}'
                self.assertEqual(
                    serializer.decode(text),
                    [{"name": "Alice", "note": "first\r\nsecond"}],
                )

    def test_encode_csv(self) -> None:
        # TODO
        pass

    def test_encode_csv_rows_with_different_keys(self) -> None:
        from benedict.serializers import CSVSerializer

        serializer = CSVSerializer()
        self.assertEqual(
            serializer.encode([{"a": 1}, {"a": 3, "b": 2}]),
            "a,b\n1,\n3,2\n",
        )
