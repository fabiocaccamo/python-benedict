import unittest

from benedict import benedict


class benedict_keyattr_test_case(unittest.TestCase):
    def test_getitem(self):
        d = {
            "a": {
                "b": {
                    "c": "ok",
                    "d": [0, 1, 2, 3],
                    "e": [{"f": 4}, {"g": [5]}],
                },
            },
        }
        b = benedict(d, keyattr_enabled=True)
        self.assertEqual(b.a.b.c, "ok")
        self.assertEqual(b.a.b.d[-1], 3)
        self.assertEqual(b.a.b.e[0].f, 4)
        self.assertEqual(b.a.b.e[-1].g[0], 5)

    def test_getitem_with_non_existing_key(self):
        d = {
            "a": "ok",
        }
        b = benedict(d, keyattr_enabled=True)
        self.assertEqual(b.b, {})

    def test_getitem_with_non_existing_protected_item(self):
        d = {
            "a": {
                "b": {
                    "c": "ok",
                },
            },
        }
        b = benedict(d, keyattr_enabled=True)
        self.assertEqual(b.a.b.c, "ok")
        with self.assertRaises(AttributeError):
            b.__test__()
        with self.assertRaises(AttributeError):
            b.a.b.__test__()

    def test_getitem_with_keyattr_disabled(self):
        d = {
            "a": "ok",
        }
        b = benedict(d, keyattr_enabled=False)
        with self.assertRaises(AttributeError):
            _ = b.a

    def test_setitem(self):
        d = {
            "a": {
                "b": {
                    "c": "not ok",
                    "d": [0, 1, 2, 3],
                    "e": [{"f": 4}, {"g": [5]}],
                },
            },
        }
        b = benedict(d, keyattr_enabled=True)
        b.a.b.c = "ok"
        self.assertEqual(b.a.b.c, "ok")
        b.a.b.d[-1] = 4
        self.assertEqual(b.a.b.d[-1], 4)
        b.a.b.e[0].f = 5
        self.assertEqual(b.a.b.e[0].f, 5)
        b.a.b.e[-1].g += [6]
        self.assertEqual(b.a.b.e[-1].g[-1], 6)

    def test_setitem_with_keyattr_disabled(self):
        d = {
            "a": 1,
        }
        b = benedict(d, keyattr_enabled=False)
        with self.assertRaises(AttributeError):
            b.a = 2
        with self.assertRaises(AttributeError):
            b.b = 3

    def test_setitem_with_non_existing_key(self):
        b = benedict(keyattr_enabled=True)
        b.a = "ok"
        self.assertEqual(b.a, "ok")

    def test_setitem_with_non_existing_nested_keys(self):
        b = benedict(keyattr_enabled=True)
        b.a.b.c = "ok"
        self.assertEqual(
            b,
            {
                "a": {
                    "b": {
                        "c": "ok",
                    },
                },
            },
        )

    def test_setitem_with_conflicting_key(self):
        d = {
            "items": [1, 2, 3],  # 'items' is an existing method
        }
        b = benedict(d, keyattr_enabled=True)
        with self.assertRaises(AttributeError):
            b.items.append([4, 5, 6])

    def test_keyattr_enabled_default(self):
        d = benedict()
        self.assertTrue(d.keyattr_enabled)

    def test_keyattr_enabled_from_constructor(self):
        d = benedict(keyattr_enabled=True)
        self.assertTrue(d.keyattr_enabled)
        d = benedict(keyattr_enabled=False)
        self.assertFalse(d.keyattr_enabled)

    def test_keyattr_enabled_getter_setter(self):
        d = benedict()
        d.keyattr_enabled = False
        self.assertFalse(d.keyattr_enabled)
        d.keyattr_enabled = True
        self.assertTrue(d.keyattr_enabled)
