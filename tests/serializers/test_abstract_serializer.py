import unittest
from typing import Any

from benedict.serializers import AbstractSerializer


class abstract_serializer_test_case(unittest.TestCase):
    """
    This class describes an abstract serializer test case.
    """

    def test_decode_abstract(self) -> None:
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.decode("")

    def test_encode_abstract(self) -> None:
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.encode({})

    def test_inheritance(self) -> None:
        class ConcreteSerializer(AbstractSerializer):
            @staticmethod
            def encode(d: Any, **kwargs: Any) -> str:
                return ""

        s = ConcreteSerializer()
        self.assertEqual(s.encode({}), "")
        with self.assertRaises(NotImplementedError):
            s.decode("")
