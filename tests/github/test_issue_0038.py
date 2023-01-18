import unittest

from benedict import benedict


class github_issue_0038_test_case(unittest.TestCase):
    """
    This class describes a github issue 0038 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/38

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0038
    """

    @staticmethod
    def get_dict_generator():
        yield from enumerate("abcd")

    def test_init_with_generator(self):
        b = benedict(self.get_dict_generator())
        self.assertEqual(b, {0: "a", 1: "b", 2: "c", 3: "d"})
        self.assertEqual(b.to_json(), '{"0": "a", "1": "b", "2": "c", "3": "d"}')
        # recast benedict to dict and back to benedict
        b = benedict(self.get_dict_generator())
        d = dict(b)
        b = benedict(d)
        self.assertEqual(b, {0: "a", 1: "b", 2: "c", 3: "d"})
        self.assertEqual(b.to_json(), '{"0": "a", "1": "b", "2": "c", "3": "d"}')
