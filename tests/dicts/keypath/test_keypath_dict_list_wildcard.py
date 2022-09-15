import unittest

from benedict.dicts import KeypathDict


class keypath_dict_list_wildcard_test_case(unittest.TestCase):
    def setUp(self):
        self.blueprint = KeypathDict(
            {
                "a": [
                    {"x": 1, "y": 1},
                    {"x": 2, "y": 2},
                ],
                "x": [
                    {"a": 10, "b": 10},
                    {"a": 11, "b": 11},
                ],
            }
        )

    def test_correct_wildcard(self):
        correct_wildcard_path_example = "a[*].x"
        self.assertEqual(self.blueprint[correct_wildcard_path_example], [1, 2])
