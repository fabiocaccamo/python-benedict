import unittest

from benedict.dicts.keylist import KeylistDict


class keylist_dict_test_case(unittest.TestCase):
    """
    This class describes a KeylistDict test case.
    """

    def test_contains(self):
        d = KeylistDict()
        d["a"] = {}
        d["a"]["b"] = True
        self.assertTrue(["a", "b"] in d)
        self.assertFalse(["a", "b", "c"] in d)

    def test_delitem(self):
        d = KeylistDict()
        d["a"] = {}
        d["a"]["b"] = {}
        d["a"]["b"]["c"] = True
        self.assertEqual(d.get(["a", "b", "c"]), True)
        del d[["a", "b", "c"]]
        self.assertFalse(["a", "b", "c"] in d)
        self.assertTrue(["a", "b"] in d)

    def test_get(self):
        d = KeylistDict()
        d["a"] = {}
        d["a"]["b"] = True
        self.assertEqual(d.get(["a", "b"]), True)
        self.assertEqual(d.get(["a", "b"]), True)

    def test_getitem(self):
        d = KeylistDict()
        d["a"] = {}
        d["a"]["b"] = True
        self.assertEqual(d[["a", "b"]], True)
        self.assertEqual(d[["a", "b"]], True)

    def test_pop(self):
        d = KeylistDict()
        d["a"] = {}
        d["a"]["b"] = {}
        d["a"]["b"]["c"] = True
        self.assertEqual(d.get(["a", "b", "c"]), True)
        d.pop(["a", "b", "c"])
        self.assertFalse(["a", "b", "c"] in d)
        self.assertTrue(["a", "b"] in d)

    def test_set(self):
        # TODO
        pass

    def test_setdefault(self):
        # TODO
        pass

    def test_setitem(self):
        # TODO
        pass
