from __future__ import annotations

import base64
import builtins
import datetime as dt
import os
import pickle
from typing import Any

from benedict.dicts.io import IODict

from .test_io_dict import io_dict_test_case


class io_dict_pickle_test_case(io_dict_test_case):
    """
    This class describes an IODict / pickle test case.
    """

    @staticmethod
    def _get_pickle_decoded() -> dict[str, dt.datetime]:
        return {
            "date": dt.datetime(year=1985, month=4, day=3),
        }

    @staticmethod
    def _get_pickle_encoded() -> str:
        return "gAJ9cQBYBAAAAGRhdGVxAWNkYXRldGltZQpkYXRldGltZQpxAmNfY29kZWNzCmVuY29kZQpxA1gLAAAAB8OBBAMAAAAAAABxBFgGAAAAbGF0aW4xcQWGcQZScQeFcQhScQlzLg=="

    def test_from_pickle_with_valid_data(self) -> None:
        j = self._get_pickle_encoded()
        r = self._get_pickle_decoded()
        # static method
        d = IODict.from_pickle(j)
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)
        # constructor
        d = IODict(j, format="pickle")
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(d, r)

    def test_from_pickle_with_invalid_data(self) -> None:
        j = "Lorem ipsum est in ea occaecat nisi officia."
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(j)
        # constructor
        with self.assertRaises(ValueError):
            IODict(j, format="pickle")

    def test_from_pickle_with_valid_file_valid_content(self) -> None:
        filepath = self.input_path("valid-content.pickle")
        # static method
        d = IODict.from_pickle(filepath)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(filepath, format="pickle")
        self.assertTrue(isinstance(d, dict))
        # pickle is excluded from format autodetection
        with self.assertRaises(ValueError):
            IODict(filepath)

    def test_from_pickle_with_valid_file_valid_content_invalid_format(self) -> None:
        filepath = self.input_path("valid-content.json")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.qs")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.toml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.xml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        filepath = self.input_path("valid-content.yml")
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)

    def test_from_pickle_with_valid_file_invalid_content(self) -> None:
        filepath = self.input_path("invalid-content.pickle")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="pickle")

    def test_from_pickle_with_invalid_file(self) -> None:
        filepath = self.input_path("invalid-file.pickle")
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(filepath)
        # constructor
        with self.assertRaises(ValueError):
            IODict(filepath, format="pickle")

    def test_from_pickle_with_valid_url_valid_content(self) -> None:
        url = self.input_url("valid-content.pickle")
        # static method
        d = IODict.from_pickle(url)
        self.assertTrue(isinstance(d, dict))
        # constructor
        d = IODict(url, format="pickle")
        self.assertTrue(isinstance(d, dict))
        # pickle is excluded from format autodetection
        with self.assertRaises(ValueError):
            IODict(url)

    def test_from_pickle_with_valid_url_invalid_content(self) -> None:
        url = "https://github.com/fabiocaccamo/python-benedict"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="pickle")

    def test_from_pickle_with_invalid_url(self) -> None:
        url = "https://github.com/fabiocaccamo/python-benedict-invalid"
        # static method
        with self.assertRaises(ValueError):
            IODict.from_pickle(url)
        # constructor
        with self.assertRaises(ValueError):
            IODict(url, format="pickle")

    def test_to_pickle(self) -> None:
        d = IODict(self._get_pickle_decoded())
        s = d.to_pickle()
        self.assertEqual(IODict.from_pickle(s), self._get_pickle_decoded())

    def test_to_pickle_file(self) -> None:
        d = IODict({"date": self._get_pickle_decoded()})
        filepath = self.output_path("test_to_pickle_file.pickle")
        d.to_pickle(filepath=filepath)
        self.assertFileExists(filepath)
        self.assertEqual(d, IODict.from_pickle(filepath))

    def test_init_with_pickle_path_without_format_does_not_execute_code(self) -> None:
        marker = self.output_path("autodetect-pickle-marker")
        if os.path.exists(marker):
            os.remove(marker)
        code = "open(" + repr(marker) + ", 'w').write('executed')"

        class Payload:
            def __reduce__(self) -> tuple[Any, ...]:
                return (builtins.exec, (code,))

        filepath = self.output_path("autodetect-pickle-payload.pickle")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            file.write(base64.b64encode(pickle.dumps(Payload())).decode())

        with self.assertRaises(ValueError):
            IODict(filepath)
        self.assertFalse(
            os.path.exists(marker),
            "the pickle payload was decoded and executed",
        )

        # ...while an explicit format still decodes pickle
        d = IODict(self.input_path("valid-content.pickle"), format="pickle")
        self.assertTrue(isinstance(d, dict))
