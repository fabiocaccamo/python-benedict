import unittest

from benedict.dicts import KeylistDict, KeypathDict


class frozen_assignment_test_case(unittest.TestCase):
    def test_frozen_nested_assignment(self) -> None:
        for cls, key in [
            (KeylistDict, ["nested", "value"]),
            (KeypathDict, "nested.value"),
        ]:
            for data in [{"nested": {"value": 1}}, {"nested": {}}, {}]:
                with self.subTest(cls=cls, data=data):
                    obj = cls(data).freeze()
                    before = repr(obj)
                    with self.assertRaises(TypeError):
                        obj[key] = 2
                    self.assertEqual(repr(obj), before)

    def test_frozen_list_assignment(self) -> None:
        obj = KeylistDict({"items": [1]}).freeze()
        with self.assertRaises(TypeError):
            obj[["items", 0]] = 2
        self.assertEqual(obj["items"], [1])

    def test_assignment_after_unfreeze(self) -> None:
        obj = KeypathDict({"nested": {"value": 1}}).freeze().unfreeze()
        obj["nested.value"] = 2
        self.assertEqual(obj["nested.value"], 2)
