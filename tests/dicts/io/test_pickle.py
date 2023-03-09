import pickle
import unittest

from benedict import benedict


class pickle_test_case(unittest.TestCase):
    """
    This class describes a pickle test case.
    """

    def test_pickle(self):
        d = {
            "a": {},
            "b": {"x": 1},
            "c": [],
            "d": [0, 1],
            "e": 0.0,
            "f": "",
            "g": None,
            "h": "0",
            "i": benedict({"h": True}),
        }
        b = benedict(
            d,
            keyattr_enabled=False,
            keypath_separator="/",
        )
        b_encoded = pickle.dumps(b)
        # print(b_encoded)
        b_decoded = pickle.loads(b_encoded)
        # print(b_decoded)
        # print(b_decoded.keypath_separator)
        self.assertTrue(isinstance(b_decoded, benedict))
        self.assertEqual(b_decoded.keyattr_enabled, b.keyattr_enabled)
        self.assertEqual(b_decoded.keypath_separator, b.keypath_separator)
        self.assertEqual(b_decoded, b)
