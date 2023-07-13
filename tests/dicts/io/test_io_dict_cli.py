from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_cli_test_case(io_dict_test_case):
    """
    This class describes an IODict / cli test case.
    """

    def test_from_cli_with_valid_data(self):
        s = """--url "https://github.com" --usernames another handle --languages Python --languages JavaScript -v --count --count --count"""
        # static method
        r = {
            "url": '"https://github.com"',
            "usernames": ["another", "handle"],
            "languages": ["Python", "JavaScript"],
            "v": True,
            "count": 3,
        }

        d = IODict.from_cli(s)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(s, format="cli")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_cli_with_invalid_arguments(self):
        s = """--help -h"""

        # static method
        with self.assertRaises(ValueError):
            IODict.from_cli(s)
        # constructor
        with self.assertRaises(ValueError):
            IODict(s, format="cli")

    def test_from_cli_with_invalid_data(self):
        s = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_cli(s)
        # constructor
        with self.assertRaises(ValueError):
            IODict(s, format="cli")
