import datetime as dt
import unittest

from benedict.serializers import PickleSerializer
from benedict.utils import type_util


class pickle_serializer_test_case(unittest.TestCase):
    """
    This class describes a pickle serializer test case.
    """

    # def test_decode_pickle(self):
    #     s = 'gAJ9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAmNfY29kZWNzCmVuY29kZQpxA1gLAAAAB8OBBAMAAAAAAABxBFgGAAAAbGF0aW4xcQWGcQZScQeFcQhScQlzLg=='
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
    #     r = 'gAJ9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAmNfY29kZWNzCmVuY29kZQpxA1gLAAAAB8OBBAMAAAAAAABxBFgGAAAAbGF0aW4xcQWGcQZScQeFcQhScQlzLg=='
    #     self.assertEqual(s, r)

    def test_encode_decode_pickle(self):
        d = {
            "date": dt.datetime(year=1985, month=4, day=3),
        }
        serializer = PickleSerializer()
        s = serializer.encode(d)
        # print(s)
        self.assertTrue(type_util.is_string(s))
        r = serializer.decode(s)
        self.assertTrue(type_util.is_dict(d))
        self.assertEqual(d, r)
