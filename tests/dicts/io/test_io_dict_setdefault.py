import unittest

from benedict import benedict
from benedict.dicts.io import IODict


class io_dict_setdefault_test_case(unittest.TestCase):
    def test_json_existing_key_does_not_change_unused_default(self) -> None:
        for existing in ("42", "null", "false"):
            with self.subTest(existing=existing):
                d = IODict.from_json('{"known": ' + existing + "}")
                child = IODict.from_json('{"nested": 1}')
                fallback = {"child": child}
                expected = d["known"]

                self.assertIs(d.setdefault("known", fallback), expected)

                self.assertIs(fallback["child"], child)
                self.assertEqual(d, {"known": expected})

    def test_main_benedict_existing_key_control(self) -> None:
        d = benedict({"known": 42})
        child = benedict({"nested": 1})
        fallback = {"child": child}
        self.assertEqual(d.setdefault("known", fallback), 42)
        self.assertIs(fallback["child"], child)
