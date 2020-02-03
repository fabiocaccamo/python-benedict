# -*- coding: utf-8 -*-

from benedict.dicts.io import io_util

import unittest


class io_util_test_case(unittest.TestCase):

    def test_decode(self):
        # TODO
        pass

    def test_decode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.decode('', format='xxx')

    def test_encode(self):
        # TODO
        pass

    def test_encode_with_invalid_format(self):
        with self.assertRaises(ValueError):
            io_util.encode({}, format='xxx')

    def read_content(self):
        # TODO
        pass

    def read_file(self):
        # TODO
        pass

    def read_url(self):
        # TODO
        pass

    def write_file_dir(self):
        # TODO
        pass

    def write_file(self):
        # TODO
        pass
