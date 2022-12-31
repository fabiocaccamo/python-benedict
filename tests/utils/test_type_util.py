import unittest
from datetime import datetime
from decimal import Decimal

from benedict.utils import type_util


class type_util_test_case(unittest.TestCase):
    """
    This class describes a type utility test case.
    """

    def test_is_bool(self):
        f = type_util.is_bool
        self.assertFalse(f(None))
        self.assertTrue(f(True))
        self.assertTrue(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_collection(self):
        f = type_util.is_collection
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertTrue(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_datetime(self):
        f = type_util.is_datetime
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertTrue(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_decimal(self):
        f = type_util.is_decimal
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertTrue(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_dict(self):
        f = type_util.is_dict
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_dict_or_list(self):
        f = type_util.is_dict_or_list
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_dict_or_list_or_tuple(self):
        f = type_util.is_dict_or_list_or_tuple
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_float(self):
        f = type_util.is_float
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertTrue(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_function(self):
        f = type_util.is_function
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertTrue(f(lambda a: a))

    def test_is_integer(self):
        f = type_util.is_integer
        self.assertFalse(f(None))
        self.assertTrue(f(True))
        self.assertTrue(f(False))
        self.assertTrue(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_json_serializable(self):
        f = type_util.is_json_serializable
        self.assertTrue(f(None))
        self.assertTrue(f(True))
        self.assertTrue(f(False))
        self.assertTrue(f(int(0)))
        self.assertTrue(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertTrue(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_list(self):
        f = type_util.is_list
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_list_or_tuple(self):
        f = type_util.is_list_or_tuple
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_none(self):
        f = type_util.is_none
        self.assertTrue(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_not_none(self):
        f = type_util.is_not_none
        self.assertFalse(f(None))
        self.assertTrue(f(True))
        self.assertTrue(f(False))
        self.assertTrue(f(int(0)))
        self.assertTrue(f(float(0.5)))
        self.assertTrue(f(Decimal(0.5)))
        self.assertTrue(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertTrue(f([0, 1, 2]))
        self.assertTrue(f({0, 1, 2}))
        self.assertTrue(f({"a": 0, "b": 1, "c": 2}))
        self.assertTrue(f("hello world"))
        self.assertTrue(f(lambda a: a))

    def test_is_set(self):
        f = type_util.is_set
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertTrue(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_string(self):
        f = type_util.is_string
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertFalse(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertTrue(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_tuple(self):
        f = type_util.is_tuple
        self.assertFalse(f(None))
        self.assertFalse(f(True))
        self.assertFalse(f(False))
        self.assertFalse(f(int(0)))
        self.assertFalse(f(float(0.5)))
        self.assertFalse(f(Decimal(0.5)))
        self.assertFalse(f(datetime.now()))
        self.assertTrue(f((0, 1, 2)))
        self.assertFalse(f([0, 1, 2]))
        self.assertFalse(f({0, 1, 2}))
        self.assertFalse(f({"a": 0, "b": 1, "c": 2}))
        self.assertFalse(f("hello world"))
        self.assertFalse(f(lambda a: a))

    def test_is_uuid(self):
        f = type_util.is_uuid
        self.assertTrue(f("ca761232ed4211cebacd00aa0057b223"))
        self.assertTrue(f("CA761232-ED42-11CE-BACD-00AA0057B223"))
        self.assertTrue(f("CA761232-ED42-11CE-BACD-00AA0057B223"))
        self.assertFalse(f("CA761232-ED42-11CE-BACD-00AA0057B22X"))
        self.assertFalse(f("CA761232-ED42-11CE-BACD-00AA0057B22"))
