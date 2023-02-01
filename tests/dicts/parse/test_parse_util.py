import unittest

from benedict.dicts.parse import parse_util


class parse_util_test_case(unittest.TestCase):
    """
    This class describes a parse utility test case.
    """

    def test_parse_bool(self):
        f = parse_util.parse_bool
        self.assertTrue(f(1))
        self.assertTrue(f(True))
        self.assertTrue(f("1"))
        self.assertTrue(f("True"))
        self.assertTrue(f("Yes"))
        self.assertTrue(f("Ok"))
        self.assertTrue(f("On"))
        self.assertFalse(f(None))
        self.assertFalse(f(0))
        self.assertFalse(f(False))
        self.assertFalse(f("0"))
        self.assertFalse(f("False"))
        self.assertFalse(f("No"))
        self.assertFalse(f("Ko"))
        self.assertFalse(f("Off"))

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
        f = lambda value: parse_util.parse_list(value, separator=",")
        self.assertEqual(
            f(["0", "1", "2", "Hello World"]),
            ["0", "1", "2", "Hello World"],
        )
        self.assertEqual(f("0,1,2"), ["0", "1", "2"])
        self.assertEqual(f("0"), ["0"])
        self.assertEqual(f("1"), ["1"])
        self.assertEqual(f(""), None)
        self.assertEqual(f(None), None)

    def test_parse_list_with_valid_json(self):
        f = lambda value: parse_util.parse_list(value, separator=None)
        self.assertEqual(f("[0,1,2,3]"), [0, 1, 2, 3])

    def test_parse_list_with_invalid_json_with_separator(self):
        f = lambda value: parse_util.parse_list(value, separator=",")
        self.assertEqual(f("[a,b,c]"), ["[a", "b", "c]"])

    def test_parse_list_with_invalid_json_without_separator(self):
        f = lambda value: parse_util.parse_list(value, separator=None)
        self.assertEqual(f("[a,b,c]"), None)

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
