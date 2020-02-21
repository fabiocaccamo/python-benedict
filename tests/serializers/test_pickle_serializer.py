# -*- coding: utf-8 -*-

from benedict.serializers import PickleSerializer
from benedict.utils import type_util

import datetime as dt
import unittest


class pickle_serializer_test_case(unittest.TestCase):

    # def test_decode_pickle(self):
    #     s = 'gAN9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAkMKB8EEAwAAAAAAAHEDhXEEUnEFcy4='
    #     d = PickleSerializer().decode(s)
    #     r = {
    #         'date': dt.datetime(year=1985, month=4, day=3),
    #     }
    #     self.assertEqual(d, r)

    # def test_encode_pickle(self):
    #     d = {
    #         'date': dt.datetime(year=1985, month=4, day=3),
    #     }
    #     s = PickleSerializer().encode(d)
    #     r = 'gAN9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAkMKB8EEAwAAAAAAAHEDhXEEUnEFcy4='
    #     self.assertEqual(s, r)

    def test_encode_decode_pickle(self):
        d = {
            'date': dt.datetime(year=1985, month=4, day=3),
        }
        serializer = PickleSerializer()
        s = serializer.encode(d)
        print(s)
        self.assertTrue(type_util.is_string(s))
        r = serializer.decode(s)
        self.assertTrue(type_util.is_dict(d))
        self.assertEqual(d, r)
