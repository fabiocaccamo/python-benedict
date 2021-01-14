# -*- coding: utf-8 -*-

from benedict.dicts.parse import parse_util

import unittest


class parse_util_test_case(unittest.TestCase):

    def test_parse_bool(self):
        f = parse_util.parse_bool
        self.assertTrue(f(1))
        self.assertTrue(f(True))
        self.assertTrue(f('1'))
        self.assertTrue(f('True'))
        self.assertTrue(f('Yes'))
        self.assertTrue(f('Ok'))
        self.assertTrue(f('On'))
        self.assertFalse(f(None))
        self.assertFalse(f(0))
        self.assertFalse(f(False))
        self.assertFalse(f('0'))
        self.assertFalse(f('False'))
        self.assertFalse(f('No'))
        self.assertFalse(f('Ko'))
        self.assertFalse(f('Off'))

    def test_parse_date(self):
        # TODO
        pass

    def test_parse_datetime(self):
        # TODO
        pass

    def test_parse_decimal(self):
        # TODO
        pass

    def test_parse_dict(self):
        # TODO
        pass

    def test_parse_float(self):
        # TODO
        pass

    def test_parse_email(self):
        # TODO
        pass

    def test_parse_int(self):
        # TODO
        pass

    def test_parse_list(self):
        f = lambda value: parse_util.parse_list(value, separator=',')
        self.assertEqual(f(['0', '1', '2', 'Hello World']), ['0', '1', '2', 'Hello World'])
        self.assertEqual(f('0,1,2'), ['0', '1', '2'])
        self.assertEqual(f('0'), ['0'])
        self.assertEqual(f('1'), ['1'])
        self.assertEqual(f(''), None)
        self.assertEqual(f(None), None)

    def test_parse_phonenumber(self):
        # TODO
        pass

    def test_parse_slug(self):
        # TODO
        pass

    def test_parse_str(self):
        # TODO
        pass

    def test_parse_uuid(self):
        # TODO
        pass
