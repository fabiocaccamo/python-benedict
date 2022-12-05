import unittest

from benedict.core import search as _search


class search_test_case(unittest.TestCase):
    """
    This class describes a search test case.
    """

    def test_search_string(self):
        d = {
            "a": "Hello world",
            "b": "Hello world!",
            "c": {
                "d": True,
                "e": " hello world ",
                "f": {
                    "g": "HELLO",
                    "h": 12345,
                    "hello": True,
                },
            },
            "u": 5,
            "v": {
                "x": {
                    "y": 5,
                    "z": 6,
                },
            },
            "Hello world": "Hello World",
        }

        results = _search(
            d, "Hello", in_keys=False, in_values=False, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

        results = _search(
            d, "Hello", in_keys=False, in_values=True, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

        results = _search(
            d, "Hello", in_keys=False, in_values=True, exact=True, case_sensitive=False
        )
        self.assertEqual(len(results), 1)
        self.assertTrue(
            (
                d["c"]["f"],
                "g",
                d["c"]["f"]["g"],
            )
            in results
        )

        results = _search(
            d, "hello", in_keys=True, in_values=True, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 6)
        self.assertTrue(
            (
                d,
                "a",
                d["a"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "b",
                d["b"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"],
                "e",
                d["c"]["e"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"]["f"],
                "g",
                d["c"]["f"]["g"],
            )
            in results
        )
        self.assertTrue(
            (
                d["c"]["f"],
                "hello",
                d["c"]["f"]["hello"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "Hello world",
                d["Hello world"],
            )
            in results
        )

        results = _search(
            d, "hello", in_keys=True, in_values=False, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 2)
        self.assertTrue(
            (
                d["c"]["f"],
                "hello",
                d["c"]["f"]["hello"],
            )
            in results
        )
        self.assertTrue(
            (
                d,
                "Hello world",
                d["Hello world"],
            )
            in results
        )

    def test_search_int(self):
        d = {
            "u": 5,
            "v": {
                "x": {
                    "y": 5,
                    "z": 6,
                },
            },
            "w": "5",
            5: 5,
            "5": "5 str",
        }

        results = _search(
            d, 5, in_keys=False, in_values=False, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

        results = _search(
            d, 5, in_keys=False, in_values=True, exact=True, case_sensitive=True
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(
            (
                d,
                "u",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d["v"]["x"],
                "y",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d,
                5,
                5,
            )
            in results
        )

        results = _search(
            d, 5, in_keys=False, in_values=True, exact=True, case_sensitive=False
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(
            (
                d,
                "u",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d["v"]["x"],
                "y",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d,
                5,
                5,
            )
            in results
        )

        results = _search(
            d, 5, in_keys=True, in_values=True, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(
            (
                d,
                "u",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d["v"]["x"],
                "y",
                5,
            )
            in results
        )
        self.assertTrue(
            (
                d,
                5,
                5,
            )
            in results
        )

        results = _search(
            d, 5, in_keys=True, in_values=False, exact=False, case_sensitive=False
        )
        self.assertEqual(len(results), 1)
        self.assertTrue(
            (
                d,
                5,
                5,
            )
            in results
        )
