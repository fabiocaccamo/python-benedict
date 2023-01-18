import unittest

from benedict.serializers import AbstractSerializer


class abstract_serializer_test_case(unittest.TestCase):
    """
    This class describes an abstract serializer test case.
    """

    def test_decode_abstract(self):
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.decode("")

    def test_encode_abstract(self):
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.encode({})

    def test_inheritance(self):
        class ConcreteSerializer(AbstractSerializer):
            @staticmethod
            def encode(d):
                return ""

        s = ConcreteSerializer()
        self.assertEqual(s.encode({}), "")
        with self.assertRaises(NotImplementedError):
            s.decode("")
