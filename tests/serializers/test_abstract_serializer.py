# -*- coding: utf-8 -*-

from benedict.serializers import AbstractSerializer

import unittest


class abstract_serializer_test_case(unittest.TestCase):

    def test_decode_abstract(self):
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.decode('')

    def test_encode_abstract(self):
        s = AbstractSerializer()
        with self.assertRaises(NotImplementedError):
            s.encode({})
