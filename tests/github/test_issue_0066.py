import unittest

from benedict import benedict


class github_issue_0066_test_case(unittest.TestCase):
    """
    This class describes a github issue 0066 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/66

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0066
    """

    def _get_dict(self):
        d = benedict(
            {
                "results": [
                    {
                        "locations": (1, 2, 3),
                    },
                    {
                        "locations": (4, 5, 6),
                    },
                    {
                        "locations": (7, 8, 9),
                    },
                    {
                        "locations": (10, 11, 12),
                    },
                ]
            }
        )
        return d

    def test_contains_with_tuple(self):
        d = self._get_dict()
        self.assertTrue("results[-1].locations[-1]" in d)
        self.assertFalse("results[-1].locations[3]" in d)

    def test_get_item_with_tuple(self):
        d = self._get_dict()
        loc = d["results[-1].locations[-1]"]
        self.assertEqual(loc, 12)

    def test_get_with_tuple(self):
        d = self._get_dict()
        loc = d.get("results[-1].locations[-1]")
        self.assertEqual(loc, 12)

    def test_delete_item_with_tuple(self):
        d = self._get_dict()
        with self.assertRaises(TypeError):
            del d["results[-1].locations[-1]"]
        # del d['results[-1].locations[-1]']
        # loc = d.get('results[-1].locations[-1]')
        # self.assertEqual(loc, 11)

    def test_delete_item_with_tuple_at_root_level(self):
        d = benedict(
            {
                "locations": (10, 11, 12),
            }
        )
        with self.assertRaises(TypeError):
            del d["locations[-1]"]
        # del d['locations[-1]']
        # loc = d.get('locations[-1]')
        # self.assertEqual(loc, 11)
        # self.assertEqual(len(d.get('locations')), 2)

    def test_pop_with_tuple(self):
        d = self._get_dict()
        with self.assertRaises(TypeError):
            loc = d.pop("results[-1].locations[-1]")
        # loc = d.pop('results[-1].locations[-1]')
        # self.assertEqual(loc, 12)
        # self.assertEqual(len(d.get('results[-1].locations')), 2)
        # loc = d.get('results[-1].locations[-1]')
        # self.assertEqual(loc, 11)

    def test_set_item_with_tuple(self):
        d = self._get_dict()
        with self.assertRaises(TypeError):
            d["results[-1].locations[-1]"] = 13
        # self.assertEqual(len(d.get('results[-1].locations')), (10, 11, 13, ))
        # self.assertEqual(len(d.get('results[-1].locations')), 3)
        # loc = d.get('results[-1].locations[-1]')
        # self.assertEqual(loc, 13)
