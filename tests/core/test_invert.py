import unittest

from benedict.core import invert as _invert


class invert_test_case(unittest.TestCase):
    """
    This class describes an invert test case.
    """

    def test_invert_with_unique_values(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        o = _invert(i)
        r = {
            1: ["a"],
            2: ["b"],
            3: ["c"],
            4: ["d"],
            5: ["e"],
        }
        self.assertEqual(o, r)

    def test_invert_with_flat_unique_values(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
        }
        o = _invert(i, flat=True)
        r = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
        }
        self.assertEqual(o, r)

    def test_invert_with_multiple_values(self):
        i = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 1,
            "e": 2,
            "f": 3,
        }
        o = _invert(i)
        self.assertTrue("a" and "d" in o[1])
        self.assertTrue("b" and "e" in o[2])
        self.assertTrue("c" and "f" in o[3])

    def test_invert_with_list_values(self):
        i = {
            "a": [
                "x",
                "y",
                "z",
            ],
            "b": [
                "c",
                "d",
                "e",
            ],
        }
        o = _invert(i)
        r = {
            "x": ["a"],
            "y": ["a"],
            "z": ["a"],
            "c": ["b"],
            "d": ["b"],
            "e": ["b"],
        }
        self.assertEqual(o, r)
        ii = _invert(o)
        # self.assertEqual(i_back, i)
        self.assertTrue("a" in ii)
        self.assertTrue("b" in ii)
        self.assertEqual(len(ii.keys()), 2)
        self.assertTrue("x" in ii["a"])
        self.assertTrue("y" in ii["a"])
        self.assertTrue("z" in ii["a"])
        self.assertEqual(len(ii["a"]), 3)
        self.assertTrue("c" in ii["b"])
        self.assertTrue("d" in ii["b"])
        self.assertTrue("e" in ii["b"])
        self.assertEqual(len(ii["b"]), 3)

    def test_invert_with_tuple_values(self):
        i = {
            "a": (
                "x",
                "y",
                "z",
            ),
            "b": (
                "c",
                "d",
                "e",
            ),
        }
        o = _invert(i)
        r = {
            "x": [
                "a",
            ],
            "y": [
                "a",
            ],
            "z": [
                "a",
            ],
            "c": [
                "b",
            ],
            "d": [
                "b",
            ],
            "e": [
                "b",
            ],
        }
        self.assertEqual(o, r)
