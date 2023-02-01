import unittest

from benedict import benedict


class github_issue_0109_test_case(unittest.TestCase):
    """
    This class describes a github issue 0102 test case.
    https://github.com/fabiocaccamo/python-benedict/issues/109

    To run this specific test:
    - Run python -m unittest tests.github.test_issue_0109
    """

    def test_set_dict_item_value_in_list(self):
        d = benedict()
        d["a"] = "1"
        d["b[1]"] = "a"
        d["c.d[3]"] = "b"
        # d["e.f[4]"] = {}
        d["e.f[4].g"] = "c"
        d["e.f[4].g.h.i[-1].l.m"] = "d"
        # print(d.dump())
