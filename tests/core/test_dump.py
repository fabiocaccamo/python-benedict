# -*- coding: utf-8 -*-

from benedict.core import dump as _dump
from decimal import Decimal

import datetime as dt
import unittest


class dump_test_case(unittest.TestCase):

    def test_dump(self):
        d = {
            'a': {
                'b': {
                    'c': 1
                }
            }
        }
        r = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        o = _dump(d)
        self.assertEqual(o, r)

    def test_dump_with_datetime(self):
        d = {
            'datetime': dt.datetime(2019, 6, 11),
        }
        r = """{
    "datetime": "2019-06-11 00:00:00"
}"""
        o = _dump(d)
        self.assertEqual(o, r)

    def test_dump_with_decimal(self):
        d = {
            'decimal': Decimal('1.75'),
        }
        r = """{
    "decimal": "1.75"
}"""
        o = _dump(d)
        self.assertEqual(o, r)
