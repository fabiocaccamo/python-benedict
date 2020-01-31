# -*- coding: utf-8 -*-

from benedict.utils import io_util

import unittest


class io_util_test_case(unittest.TestCase):

    def test_decode(self):
        pass

    def test_decode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.decode('', format='xxx')

    def test_encode(self):
        pass

    def test_encode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.encode({}, format='xxx')

    def read_content(self):
        pass

    def read_file(self):
        pass

    def read_url(self):
        pass

    def write_file_dir(self):
        pass

    def write_file(self):
        pass
