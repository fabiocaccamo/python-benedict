# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict

import os
import shutil
import unittest


class io_dict_test_case(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        dir_path = cls.output_path(filepath='')
        shutil.rmtree(dir_path, ignore_errors=True)

    @staticmethod
    def input_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'input/{}'.format(filepath))

    @staticmethod
    def input_url(filepath):
        return 'https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/dicts/io/input/{}'.format(filepath)

    @staticmethod
    def output_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, 'output/{}'.format(filepath))

    def assertFileExists(self, filepath):
        self.assertTrue(os.path.isfile(filepath))

    def test_init_with_invalid_data(self):
        with self.assertRaises(ValueError):
            d = IODict('invalid json data')
