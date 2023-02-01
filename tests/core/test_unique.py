import unittest

from benedict.core import unique as _unique


class unique_test_case(unittest.TestCase):
    """
    This class describes an unique test case.
    """

    def test_unique(self):
        d = {
            "a": {
                "x": 1,
                "y": 1,
            },
            "b": {
                "x": 2,
                "y": 2,
            },
            "c": {
                "x": 1,
                "y": 1,
            },
            "d": {
                "x": 1,
            },
            "e": {
                "x": 1,
                "y": 1,
                "z": 1,
            },
            "f": {
                "x": 2,
                "y": 2,
            },
        }
        _unique(d)
        rv = [
            {
                "x": 1,
                "y": 1,
            },
            {
                "x": 2,
                "y": 2,
            },
            {
                "x": 1,
            },
            {
                "x": 1,
                "y": 1,
                "z": 1,
            },
        ]
        self.assertEqual(len(d.keys()), len(rv))
        self.assertTrue(all([value in rv for value in d.values()]))
