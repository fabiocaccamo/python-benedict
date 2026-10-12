import unittest

from benedict.core import clone as _clone


class clone_test_case(unittest.TestCase):
    """
    This class describes a clone test case.
    """

    def test_clone(self) -> None:
        i = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        o = _clone(i)
        self.assertEqual(type(i), type(o))
        self.assertEqual(i, o)
        self.assertFalse(i is o)
        o["a"]["b"]["c"] = 2
        self.assertEqual(i["a"]["b"]["c"], 1)
        self.assertEqual(o["a"]["b"]["c"], 2)

    def test_clone_empty(self) -> None:
        i = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        o = _clone(i, empty=True)
        self.assertEqual(type(i), type(o))
        self.assertEqual(o, {})

    def test_clone_empty_does_not_call_custom_unfreeze(self) -> None:
        class MappingWithUnfreeze(dict):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.unfreeze_calls = 0

            def unfreeze(self):
                self.unfreeze_calls += 1

        i = MappingWithUnfreeze({"a": 1})

        o = _clone(i, empty=True)

        self.assertIsInstance(o, MappingWithUnfreeze)
        self.assertEqual(o, {})
        self.assertEqual(o.unfreeze_calls, 0)
