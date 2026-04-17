from __future__ import annotations

import importlib
import json
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


class schema_util_test_case(unittest.TestCase):
    def test_apply_schema_valid(self) -> None:
        data = {"name": "Alice", "age": 30}
        result = schema_util.apply_schema(data, UserSchema)
        self.assertEqual(result, {"name": "Alice", "age": 30})

    def test_apply_schema_coerces_types(self) -> None:
        data = {"name": "Bob", "age": "25"}
        result = schema_util.apply_schema(data, UserSchema)
        self.assertEqual(result, {"name": "Bob", "age": 25})
        self.assertIsInstance(result["age"], int)

    def test_apply_schema_strips_extra_fields(self) -> None:
        # Fields not declared in the schema must be absent from the result.
        data = {"name": "Alice", "age": 30, "email": "alice@example.com", "extra": 42}
        result = schema_util.apply_schema(data, UserSchema)
        self.assertEqual(result, {"name": "Alice", "age": 30})
        self.assertNotIn("email", result)
        self.assertNotIn("extra", result)

    def test_apply_schema_missing_required_field_raises(self) -> None:
        # A missing required field must raise a ValidationError.
        data = {"name": "Alice"}  # 'age' is required but absent
        with self.assertRaises(pydantic.ValidationError):
            schema_util.apply_schema(data, UserSchema)

    def test_apply_schema_invalid_data_raises(self) -> None:
        data = {"name": "Charlie", "age": "not-a-number"}
        with self.assertRaises(pydantic.ValidationError):
            schema_util.apply_schema(data, UserSchema)

    def test_apply_schema_pydantic_not_installed_raises(self) -> None:
        with patch.object(schema_util, "pydantic_installed", False):
            with self.assertRaises(ExtrasRequireModuleNotFoundError):
                schema_util.apply_schema({"name": "X", "age": 1}, UserSchema)

    def test_pydantic_not_installed_at_import_time(self) -> None:
        module_key = "benedict.utils.schema_util"
        original_module = sys.modules.pop(module_key, None)
        try:
            with patch.dict("sys.modules", {"pydantic": None}):
                reimported = importlib.import_module(module_key)
                self.assertFalse(reimported.pydantic_installed)
        finally:
            if original_module is not None:
                sys.modules[module_key] = original_module


class schema_extras_test_case(unittest.TestCase):
    def test_require_schema_error_message(self) -> None:
        from benedict.extras import require_schema

        with self.assertRaises(ExtrasRequireModuleNotFoundError) as ctx:
            require_schema(installed=False)
        self.assertIn("schema", str(ctx.exception))
        self.assertIn("python-benedict[schema]", str(ctx.exception))


class io_dict_from_json_schema_test_case(unittest.TestCase):
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

    def test_from_json_with_schema_strips_extra_fields(self) -> None:
        j = '{"name": "Alice", "age": 30, "email": "alice@example.com"}'
        d = IODict.from_json(j, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_json_with_schema_missing_required_field_raises(self) -> None:
        j = '{"name": "Alice"}'  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_json(j, schema=UserSchema)

    def test_from_json_without_schema(self) -> None:
        j = '{"name": "Alice", "age": 30}'
        d = IODict.from_json(j)
        self.assertEqual(d, {"name": "Alice", "age": 30})


class io_dict_from_yaml_schema_test_case(unittest.TestCase):
    def test_from_yaml_with_schema_valid(self) -> None:
        y = "name: Alice\nage: 30\n"
        d = IODict.from_yaml(y, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_yaml_with_schema_strips_extra_fields(self) -> None:
        y = "name: Alice\nage: 30\nemail: alice@example.com\n"
        d = IODict.from_yaml(y, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_yaml_with_schema_missing_required_field_raises(self) -> None:
        y = "name: Alice\n"  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_yaml(y, schema=UserSchema)


class io_dict_from_ini_schema_test_case(unittest.TestCase):
    def test_from_ini_with_schema_valid(self) -> None:
        ini = "[DEFAULT]\nname = Alice\nage = 30\n"
        d = IODict.from_ini(ini, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertIsInstance(d["age"], int)


class io_dict_to_json_schema_test_case(unittest.TestCase):
    def test_to_json_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_json(schema=UserSchema)
        self.assertIn('"name": "Alice"', result)
        self.assertIn('"age": 30', result)

    def test_to_json_with_schema_coerces_types(self) -> None:
        d = benedict({"name": "Bob", "age": "25"})
        result = d.to_json(schema=UserSchema)
        parsed = json.loads(result)
        self.assertEqual(parsed["age"], 25)
        self.assertIsInstance(parsed["age"], int)

    def test_to_json_with_schema_invalid_raises(self) -> None:
        d = benedict({"name": "Charlie", "age": "not-a-number"})
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_json(schema=UserSchema)

    def test_to_json_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_json(schema=UserSchema)
        parsed = json.loads(result)
        self.assertEqual(parsed, {"name": "Alice", "age": 30})
        self.assertNotIn("email", parsed)

    def test_to_json_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_json(schema=UserSchema)

    def test_to_json_without_schema(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_json()
        self.assertIn('"name": "Alice"', result)
