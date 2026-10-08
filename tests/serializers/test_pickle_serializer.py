import datetime as dt
import unittest

from benedict.serializers import PickleSerializer, get_format_by_path
from benedict.utils import type_util


class pickle_serializer_test_case(unittest.TestCase):
    """
    This class describes a pickle serializer test case.
    """

    def test_pickle_extension_is_still_registered(self) -> None:
        # is_filepath relies on get_format_by_path to recognise a ".pickle"
        # path, unregistering the extension would break format="pickle"
        self.assertEqual(get_format_by_path("path-to/data.pickle"), "pickle")
        self.assertIn("pickle", PickleSerializer().extensions())

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

    def test_encode_decode_pickle(self) -> None:
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
