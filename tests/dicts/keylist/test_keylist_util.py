import unittest

from benedict.dicts.keylist import keylist_util


class keylist_util_test_case(unittest.TestCase):
    """
    This class describes a keylist utility test case.
    """

    def test_get_item_with_valid_keys(self):
        d = {
            "a": {
                "b": {
                    "c": [1, 2, 3],
                },
            },
        }

        item = keylist_util.get_item(d, ["a", "b"])
        self.assertEqual(
            item,
            (
                d["a"],
                "b",
                d["a"]["b"],
            ),
        )

        item = keylist_util.get_item(d, ["a", "b", "c"])
        self.assertEqual(
            item,
            (
                d["a"]["b"],
                "c",
                [1, 2, 3],
            ),
        )

        item = keylist_util.get_item(d, ["a", "b", "c", 0])
        self.assertEqual(
            item,
            (
                d["a"]["b"]["c"],
                0,
                1,
            ),
        )

    def test_get_item_with_empty_dict(self):
        d = {}

        item = keylist_util.get_item(d, ["a"])
        self.assertEqual(
            item,
            (
                None,
                None,
                None,
            ),
        )

        item = keylist_util.get_item(d, ["a", "b"])
        self.assertEqual(
            item,
            (
                None,
                None,
                None,
            ),
        )

        item = keylist_util.get_item(d, ["a", 0])
        self.assertEqual(
            item,
            (
                None,
                None,
                None,
            ),
        )

    def test_get_item_with_empty_keys(self):
        d = {}

        item = keylist_util.get_item(d, [])
        self.assertEqual(
            item,
            (
                None,
                None,
                None,
            ),
        )

    def test_set_item_with_indexes(self):
        d = {}

        keylist_util.set_item(d, "a", None)
        self.assertEqual(d, {"a": None})

        keylist_util.set_item(d, ["a", "b", "c"], 0)
        self.assertEqual(d, {"a": {"b": {"c": 0}}})

        keylist_util.set_item(d, ["a", "b", "d"], 1)
        self.assertEqual(d, {"a": {"b": {"c": 0, "d": 1}}})

        keylist_util.set_item(d, ["a", "b", "e", 0], 1)
        keylist_util.set_item(d, ["a", "b", "e", 1], 2)
        keylist_util.set_item(d, ["a", "b", "e", 2], 3)
        self.assertEqual(d, {"a": {"b": {"c": 0, "d": 1, "e": [1, 2, 3]}}})

        keylist_util.set_item(d, ["a", "b", "e", 0], 4)
        keylist_util.set_item(d, ["a", "b", "e", 1], 5)
        keylist_util.set_item(d, ["a", "b", "e", 2], 6)
        # keylist_util.set_item(d, ['a', 'b', 'e', 3], 7)
        # keylist_util.set_item(d, ['a', 'b', 'e', 4], 8)
        keylist_util.set_item(d, ["a", "b", "e", 5], 9)
        self.assertEqual(
            d,
            {
                "a": {
                    "b": {
                        "c": 0,
                        "d": 1,
                        "e": [4, 5, 6, None, None, 9],
                    },
                },
            },
        )
        keylist_util.set_item(d, ["a", "b", "e", -11], 10)
        self.assertEqual(
            d,
            {
                "a": {
                    "b": {
                        "c": 0,
                        "d": 1,
                        "e": [10, 4, 5, 6, None, None, 9],
                    },
                },
            },
        )
