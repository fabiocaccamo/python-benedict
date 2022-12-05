import os
import shutil
import unittest

from benedict.dicts.io import IODict


class io_dict_test_case(unittest.TestCase):
    """
    This class describes an IODict test case.
    """

    @classmethod
    def tearDownClass(cls):
        dir_path = cls.output_path(filepath="")
        shutil.rmtree(dir_path, ignore_errors=True)

    @staticmethod
    def input_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, f"input/{filepath}")

    @staticmethod
    def input_url(filepath):
        return f"https://raw.githubusercontent.com/fabiocaccamo/python-benedict/master/tests/dicts/io/input/{filepath}"

    @staticmethod
    def output_path(filepath):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, f"output/{filepath}")

    def assertFileExists(self, filepath):
        self.assertTrue(os.path.isfile(filepath))

    def test_init_with_key_value_list(self):
        d = IODict(a="1", b="2", c="3")
        self.assertEqual(
            d,
            {
                "a": "1",
                "b": "2",
                "c": "3",
            },
        )

    def test_init_with_invalid_data(self):
        with self.assertRaises(ValueError):
            d = IODict("invalid json data")
