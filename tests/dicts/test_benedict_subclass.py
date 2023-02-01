import unittest

from benedict import benedict


class subbenedict(benedict):
    pass


class benedict_subclass_test_case(unittest.TestCase):
    """
    This class describes a benedict subclass test case.
    """

    def test_cast(self):
        d = subbenedict(
            {
                "a": {
                    "b": {
                        "c": {
                            "d": True,
                        },
                    }
                }
            }
        )
        c = d["a.b.c"]
        self.assertTrue(issubclass(type(c), benedict))
        self.assertTrue(isinstance(c, subbenedict))
        self.assertEqual(c, {"d": True})

    def test_clone(self):
        d = subbenedict({"a": True})
        c = d.clone()
        self.assertTrue(issubclass(type(c), benedict))
        self.assertTrue(isinstance(c, subbenedict))
        self.assertEqual(c, {"a": True})
