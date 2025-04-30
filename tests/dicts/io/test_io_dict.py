import os
import shutil
import unittest

from benedict.dicts.io import IODict


class io_dict_test_case(unittest.TestCase):
    """
    This class describes an IODict test case.
    """

    @classmethod
    def tearDownClass(cls) -> None:
        dir_path = cls.output_path(filepath="")
        shutil.rmtree(dir_path, ignore_errors=True)

    @staticmethod
    def input_path(filepath: str) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, f"input/{filepath}")

    @staticmethod
    def input_url(filepath: str) -> str:
        return f"https://raw.githubusercontent.com/fabiocaccamo/python-benedict/main/tests/dicts/io/input/{filepath}"

    @staticmethod
    def output_path(filepath: str) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, f"output/{filepath}")

    def assertFileExists(self, filepath: str) -> None:
        self.assertTrue(os.path.isfile(filepath))

    def test_init_with_key_value_list(self) -> None:
        d = IODict(a="1", b="2", c="3")
        self.assertEqual(
            d,
            {
                "a": "1",
                "b": "2",
                "c": "3",
            },
        )

    def test_init_with_invalid_data(self) -> None:
        with self.assertRaises(ValueError):
            _ = IODict("invalid json data")
