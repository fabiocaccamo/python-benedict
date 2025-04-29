import datetime as dt
import unittest
from typing import Any

from benedict.core import dump as _dump


class dump_test_case(unittest.TestCase):
    """
    This class describes a dump test case.
    """

    @staticmethod
    def _rstrip_lines(s: str) -> str:
        return "\n".join([line.rstrip() for line in s.splitlines()])

    def test_dump(self) -> None:
        d = {
            "a": {
                "b": {
                    "c": 1,
                },
            },
        }
        r = """{
    "a": {
        "b": {
            "c": 1
        }
    }
}"""
        o = _dump(d)
        self.assertEqual(self._rstrip_lines(o), r)

    def test_dump_with_datetime(self) -> None:
        d = {
            "datetime": dt.datetime(2019, 6, 11),
        }
        r = """{
    "datetime": "2019-06-11T00:00:00"
}"""
        o = _dump(d)
        self.assertEqual(self._rstrip_lines(o), r)

    def test_dump_with_set(self) -> None:
        d = {
            "set": {0, 1, 2, 3, 4, 5},
        }
        r = """{
    "set": [
        0,
        1,
        2,
        3,
        4,
        5
    ]
}"""
        o = _dump(d)
        self.assertEqual(self._rstrip_lines(o), r)

    def test_dump_with_unsortable_keys(self) -> None:
        d: dict[Any, Any] = {
            None: None,
            0: 0,
            1: 1,
        }
        # must not raise TypeError
        _dump(d)
        d["dt"] = dt
        with self.assertRaises(TypeError):
            _dump(d, sort_keys=False, default=None)
