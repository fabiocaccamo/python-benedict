import unittest

from benedict.core import clone as _clone
from benedict.core import groupby as _groupby


class groupby_test_case(unittest.TestCase):
    """
    This class describes a groupby test case.
    """

    def test_groupby(self):
        l = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Frank"},
            {"id": 3, "name": "Tony"},
            {"id": 4, "name": "Jimmy"},
            {"id": 3, "name": "Sam"},
            {"id": 1, "name": "Charles"},
            {"id": 3, "name": "Bob"},
            {"id": 4, "name": "Paul"},
            {"id": 1, "name": "Michael"},
        ]
        l_clone = _clone(l)
        d = _groupby(l, "id")
        self.assertEqual(l, l_clone)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(len(d), 4)
        self.assertTrue(
            all(
                [
                    1 in d,
                    2 in d,
                    3 in d,
                    4 in d,
                ]
            )
        )
        self.assertTrue(
            all(
                [
                    isinstance(d[1], list),
                    isinstance(d[2], list),
                    isinstance(d[3], list),
                    isinstance(d[4], list),
                ]
            )
        )
        self.assertEqual(len(d[1]), 3)
        self.assertEqual(len(d[2]), 1)
        self.assertEqual(len(d[3]), 3)
        self.assertEqual(len(d[4]), 2)

    def test_groupby_with_wrong_input(self):
        l = {"id": 1, "name": "John"}
        with self.assertRaises(ValueError):
            d = _groupby(l, "id")
        l = [
            [{"id": 1, "name": "John"}],
            [{"id": 2, "name": "Frank"}],
        ]
        with self.assertRaises(ValueError):
            d = _groupby(l, "id")
