import unittest

from benedict.core import clone as _clone


class clone_test_case(unittest.TestCase):
    """
    This class describes a clone test case.
    """

    def test_clone(self):
        i = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        o = _clone(i)
        self.assertEqual(type(i), type(o))
        self.assertEqual(i, o)
        self.assertFalse(i is o)
        o["a"]["b"]["c"] = 2
        self.assertEqual(i["a"]["b"]["c"], 1)
        self.assertEqual(o["a"]["b"]["c"], 2)

    def test_clone_empty(self):
        i = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        o = _clone(i, empty=True)
        self.assertEqual(type(i), type(o))
        self.assertEqual(o, {})
