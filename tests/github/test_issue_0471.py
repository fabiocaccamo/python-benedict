from __future__ import annotations

import importlib
import sys
import unittest
from unittest.mock import patch

import pydantic

from benedict import benedict
from benedict.dicts.io import IODict
from benedict.exceptions import ExtrasRequireModuleNotFoundError
from benedict.utils import schema_util


class UserSchema(pydantic.BaseModel):
    name: str
    age: int


class ItemSchema(pydantic.BaseModel):
    title: str
    price: float


class github_issue_0471_test_case(unittest.TestCase):
    """
    Tests for python-benedict[schema] optional dependency (pydantic-based).
    Covers apply_schema utility, from_{format} and to_{format} with schema kwarg.
    """

    # -------------------------------------------------------------------------
    # schema_util.apply_schema
    # -------------------------------------------------------------------------

    def test_apply_schema_valid(self) -> None:
        data = {"name": "Alice", "age": 30}
        result = schema_util.apply_schema(data, UserSchema)
        self.assertEqual(result, {"name": "Alice", "age": 30})

    def test_apply_schema_coerces_types(self) -> None:
        data = {"name": "Bob", "age": "25"}
        result = schema_util.apply_schema(data, UserSchema)
        self.assertEqual(result, {"name": "Bob", "age": 25})
        self.assertIsInstance(result["age"], int)

    def test_apply_schema_invalid_data_raises(self) -> None:
        data = {"name": "Charlie", "age": "not-a-number"}
        with self.assertRaises(pydantic.ValidationError):
            schema_util.apply_schema(data, UserSchema)

    def test_apply_schema_pydantic_not_installed_raises(self) -> None:
        with patch.object(schema_util, "pydantic_installed", False):
            with self.assertRaises(ExtrasRequireModuleNotFoundError):
                schema_util.apply_schema({"name": "X", "age": 1}, UserSchema)

    # -------------------------------------------------------------------------
    # from_json with schema
    # -------------------------------------------------------------------------

    def test_from_json_with_schema_valid(self) -> None:
        j = '{"name": "Alice", "age": 30}'
        d = IODict.from_json(j, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_json_with_schema_coerces_types(self) -> None:
        j = '{"name": "Bob", "age": "25"}'
        d = IODict.from_json(j, schema=UserSchema)
        self.assertIsInstance(d["age"], int)
        self.assertEqual(d["age"], 25)

    def test_from_json_with_schema_invalid_raises(self) -> None:
        j = '{"name": "Charlie", "age": "not-a-number"}'
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_json(j, schema=UserSchema)

    def test_from_json_without_schema(self) -> None:
        j = '{"name": "Alice", "age": 30}'
        d = IODict.from_json(j)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    # -------------------------------------------------------------------------
    # from_yaml with schema
    # -------------------------------------------------------------------------

    def test_from_yaml_with_schema_valid(self) -> None:
        y = "name: Alice\nage: 30\n"
        d = IODict.from_yaml(y, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    # -------------------------------------------------------------------------
    # to_json with schema
    # -------------------------------------------------------------------------

    def test_to_json_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_json(schema=UserSchema)
        self.assertIn('"name": "Alice"', result)
        self.assertIn('"age": 30', result)

    def test_to_json_with_schema_coerces_types(self) -> None:
        d = benedict({"name": "Bob", "age": "25"})
        result = d.to_json(schema=UserSchema)
        import json

        parsed = json.loads(result)
        self.assertEqual(parsed["age"], 25)
        self.assertIsInstance(parsed["age"], int)

    def test_to_json_with_schema_invalid_raises(self) -> None:
        d = benedict({"name": "Charlie", "age": "not-a-number"})
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_json(schema=UserSchema)

    def test_to_json_without_schema(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_json()
        self.assertIn('"name": "Alice"', result)

    # -------------------------------------------------------------------------
    # from_ini with schema
    # -------------------------------------------------------------------------

    def test_from_ini_with_schema_valid(self) -> None:
        ini = "[DEFAULT]\nname = Alice\nage = 30\n"
        d = IODict.from_ini(ini, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    # -------------------------------------------------------------------------
    # schema not installed error message
    # -------------------------------------------------------------------------

    def test_extras_require_schema_error_message(self) -> None:
        from benedict.extras import require_schema

        with self.assertRaises(ExtrasRequireModuleNotFoundError) as ctx:
            require_schema(installed=False)
        self.assertIn("schema", str(ctx.exception))
        self.assertIn("python-benedict[schema]", str(ctx.exception))

    def test_schema_util_pydantic_not_installed_at_import_time(self) -> None:
        """
        Simulate pydantic being unavailable at import time so that the
        'except ModuleNotFoundError' branch in schema_util is executed.
        """
        module_key = "benedict.utils.schema_util"
        original_module = sys.modules.pop(module_key, None)
        try:
            with patch.dict("sys.modules", {"pydantic": None}):
                reimported = importlib.import_module(module_key)
                self.assertFalse(reimported.pydantic_installed)
        finally:
            if original_module is not None:
                sys.modules[module_key] = original_module
