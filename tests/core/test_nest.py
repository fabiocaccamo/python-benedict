import unittest

from benedict.core import clone as _clone
from benedict.core import nest as _nest


class nest_test_case(unittest.TestCase):
    """
    This class describes a nest test case.
    """

    def test_nest(self):
        l = [
            {"id": 1, "parent_id": None, "name": "John"},
            {"id": 2, "parent_id": 1, "name": "Frank"},
            {"id": 3, "parent_id": 2, "name": "Tony"},
            {"id": 4, "parent_id": 3, "name": "Jimmy"},
            {"id": 5, "parent_id": 1, "name": "Sam"},
            {"id": 6, "parent_id": 3, "name": "Charles"},
            {"id": 7, "parent_id": 2, "name": "Bob"},
            {"id": 8, "parent_id": 3, "name": "Paul"},
            {"id": 9, "parent_id": None, "name": "Michael"},
        ]
        l_clone = _clone(l)
        n = _nest(l, "id", "parent_id", "children")
        r = [
            {
                "id": 1,
                "parent_id": None,
                "name": "John",
                "children": [
                    {
                        "id": 2,
                        "parent_id": 1,
                        "name": "Frank",
                        "children": [
                            {
                                "id": 3,
                                "parent_id": 2,
                                "name": "Tony",
                                "children": [
                                    {
                                        "id": 4,
                                        "parent_id": 3,
                                        "name": "Jimmy",
                                        "children": [],
                                    },
                                    {
                                        "id": 6,
                                        "parent_id": 3,
                                        "name": "Charles",
                                        "children": [],
                                    },
                                    {
                                        "id": 8,
                                        "parent_id": 3,
                                        "name": "Paul",
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "id": 7,
                                "parent_id": 2,
                                "name": "Bob",
                                "children": [],
                            },
                        ],
                    },
                    {
                        "id": 5,
                        "parent_id": 1,
                        "name": "Sam",
                        "children": [],
                    },
                ],
            },
            {
                "id": 9,
                "parent_id": None,
                "name": "Michael",
                "children": [],
            },
        ]
        self.assertEqual(l, l_clone)
        self.assertEqual(n, r)

    def test_nest_with_wrong_keys(self):
        l = [
            {"id": 1, "parent_id": None, "name": "John"},
            {"id": 2, "parent_id": 1, "name": "Frank"},
            {"id": 3, "parent_id": 2, "name": "Tony"},
            {"id": 4, "parent_id": 3, "name": "Jimmy"},
            {"id": 5, "parent_id": 1, "name": "Sam"},
            {"id": 6, "parent_id": 3, "name": "Charles"},
            {"id": 7, "parent_id": 2, "name": "Bob"},
            {"id": 8, "parent_id": 3, "name": "Paul"},
            {"id": 9, "parent_id": None, "name": "Michael"},
        ]
        with self.assertRaises(ValueError):
            n = _nest(l, "id", "id", "children")
        with self.assertRaises(ValueError):
            n = _nest(l, "id", "parent_id", "id")
        with self.assertRaises(ValueError):
            n = _nest(l, "id", "parent_id", "parent_id")

    def test_nest_with_wrong_input(self):
        l = {"id": 1, "parent_id": None, "name": "John"}
        with self.assertRaises(ValueError):
            d = _nest(l, "id", "parent_id", "children")
        l = [
            [{"id": 1, "parent_id": None, "name": "John"}],
            [{"id": 2, "parent_id": 1, "name": "Frank"}],
        ]
        with self.assertRaises(ValueError):
            d = _nest(l, "id", "parent_id", "children")
