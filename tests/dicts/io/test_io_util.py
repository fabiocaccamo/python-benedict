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

    def test_is_data(self):
        # TODO
        pass

    def test_is_filepath(self):
        # TODO
        pass

    def test_is_url(self):
        # TODO
        pass

    def test_read_content(self):
        # TODO
        pass

    def test_read_file(self):
        # TODO
        pass

    def test_read_url(self):
        # TODO
        pass

    def test_write_file_dir(self):
        # TODO
        pass

    def test_write_file(self):
        # TODO
        pass
