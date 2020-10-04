# -*- coding: utf-8 -*-

from benedict.serializers import INISerializer
from benedict.utils import type_util
import unittest

TARGET_DICT = {
    "section_a": {
        "b": 1,
        "c": "hếllôworlđ"
    },
    "section_b": {
        "c": 2.5,
        "d": True,
        "e": False,
    }
}

INI_STR = """[section_a]
b = 1
c = hếllôworlđ

[section_b]
c = 2.5
d = True
e = False

"""


class ini_serializer_test_case(unittest.TestCase):
    def test_decode_pickle(self):
        d = INISerializer().decode(INI_STR)
        self.assertEqual(d, TARGET_DICT)

    def test_encode_pickle(self):
        s = INISerializer().encode(TARGET_DICT)
        self.assertEqual(s, INI_STR)

    def test_encode_decode_ini(self):
        serializer = INISerializer()
        s = serializer.encode(TARGET_DICT)
        self.assertTrue(type_util.is_string(s))
        r = serializer.decode(s)
        self.assertTrue(type_util.is_dict(r))
        self.assertEqual(TARGET_DICT, r)
