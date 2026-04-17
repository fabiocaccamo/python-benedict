from __future__ import annotations

import base64
import importlib
import json
import pickle
import plistlib
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


class XMLWrappedSchema(pydantic.BaseModel):
    root: UserSchema


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

    def test_from_ini_with_schema_strips_extra_fields(self) -> None:
        ini = "[DEFAULT]\nname = Alice\nage = 30\nemail = alice@example.com\n"
        d = IODict.from_ini(ini, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_ini_with_schema_missing_required_field_raises(self) -> None:
        ini = "[DEFAULT]\nname = Alice\n"  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_ini(ini, schema=UserSchema)


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


class io_dict_from_toml_schema_test_case(unittest.TestCase):
    def test_from_toml_with_schema_valid(self) -> None:
        t = 'name = "Alice"\nage = 30\n'
        d = IODict.from_toml(t, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_toml_with_schema_strips_extra_fields(self) -> None:
        t = 'name = "Alice"\nage = 30\nemail = "alice@example.com"\n'
        d = IODict.from_toml(t, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_toml_with_schema_missing_required_field_raises(self) -> None:
        t = 'name = "Alice"\n'  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_toml(t, schema=UserSchema)


class io_dict_from_xml_schema_test_case(unittest.TestCase):
    def test_from_xml_with_schema_valid(self) -> None:
        x = "<?xml version='1.0' ?><root><name>Alice</name><age>30</age></root>"
        d = IODict.from_xml(x, schema=XMLWrappedSchema)
        self.assertEqual(d, {"root": {"name": "Alice", "age": 30}})

    def test_from_xml_with_schema_strips_extra_fields(self) -> None:
        x = "<?xml version='1.0' ?><root><name>Alice</name><age>30</age><email>alice@example.com</email></root>"
        d = IODict.from_xml(x, schema=XMLWrappedSchema)
        self.assertEqual(d, {"root": {"name": "Alice", "age": 30}})
        self.assertNotIn("email", d.get("root", {}))

    def test_from_xml_with_schema_missing_required_field_raises(self) -> None:
        x = "<?xml version='1.0' ?><root><name>Alice</name></root>"  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_xml(x, schema=XMLWrappedSchema)


class io_dict_from_base64_schema_test_case(unittest.TestCase):
    def test_from_base64_with_schema_valid(self) -> None:
        s = base64.b64encode(json.dumps({"name": "Alice", "age": 30}).encode()).decode()
        d = IODict.from_base64(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_base64_with_schema_strips_extra_fields(self) -> None:
        s = base64.b64encode(
            json.dumps({"name": "Alice", "age": 30, "email": "alice@example.com"}).encode()
        ).decode()
        d = IODict.from_base64(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_base64_with_schema_missing_required_field_raises(self) -> None:
        s = base64.b64encode(json.dumps({"name": "Alice"}).encode()).decode()
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_base64(s, schema=UserSchema)


class io_dict_from_pickle_schema_test_case(unittest.TestCase):
    def test_from_pickle_with_schema_valid(self) -> None:
        s = base64.b64encode(pickle.dumps({"name": "Alice", "age": 30}, protocol=2)).decode()
        d = IODict.from_pickle(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_pickle_with_schema_strips_extra_fields(self) -> None:
        s = base64.b64encode(
            pickle.dumps({"name": "Alice", "age": 30, "email": "alice@example.com"}, protocol=2)
        ).decode()
        d = IODict.from_pickle(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_pickle_with_schema_missing_required_field_raises(self) -> None:
        s = base64.b64encode(pickle.dumps({"name": "Alice"}, protocol=2)).decode()
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_pickle(s, schema=UserSchema)


class io_dict_from_plist_schema_test_case(unittest.TestCase):
    def test_from_plist_with_schema_valid(self) -> None:
        s = plistlib.dumps({"name": "Alice", "age": 30}).decode()
        d = IODict.from_plist(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})

    def test_from_plist_with_schema_strips_extra_fields(self) -> None:
        s = plistlib.dumps({"name": "Alice", "age": 30, "email": "alice@example.com"}).decode()
        d = IODict.from_plist(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_plist_with_schema_missing_required_field_raises(self) -> None:
        s = plistlib.dumps({"name": "Alice"}).decode()
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_plist(s, schema=UserSchema)


class io_dict_from_query_string_schema_test_case(unittest.TestCase):
    def test_from_query_string_with_schema_valid(self) -> None:
        # query strings carry all values as strings; pydantic coerces age to int
        s = "name=Alice&age=30"
        d = IODict.from_query_string(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertIsInstance(d["age"], int)

    def test_from_query_string_with_schema_strips_extra_fields(self) -> None:
        s = "name=Alice&age=30&email=alice%40example.com"
        d = IODict.from_query_string(s, schema=UserSchema)
        self.assertEqual(d, {"name": "Alice", "age": 30})
        self.assertNotIn("email", d)

    def test_from_query_string_with_schema_missing_required_field_raises(self) -> None:
        s = "name=Alice"  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            IODict.from_query_string(s, schema=UserSchema)


class io_dict_to_yaml_schema_test_case(unittest.TestCase):
    def test_to_yaml_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_yaml(schema=UserSchema)
        self.assertIsInstance(result, str)
        self.assertIn("Alice", result)
        self.assertIn("30", result)

    def test_to_yaml_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_yaml(schema=UserSchema)
        self.assertNotIn("email", result)
        self.assertIn("Alice", result)

    def test_to_yaml_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_yaml(schema=UserSchema)


class io_dict_to_ini_schema_test_case(unittest.TestCase):
    def test_to_ini_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_ini(schema=UserSchema)
        self.assertIsInstance(result, str)
        self.assertIn("Alice", result)

    def test_to_ini_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_ini(schema=UserSchema)
        self.assertNotIn("email", result)
        self.assertIn("Alice", result)

    def test_to_ini_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_ini(schema=UserSchema)


class io_dict_to_toml_schema_test_case(unittest.TestCase):
    def test_to_toml_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_toml(schema=UserSchema)
        self.assertIsInstance(result, str)
        self.assertIn("Alice", result)

    def test_to_toml_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_toml(schema=UserSchema)
        self.assertNotIn("email", result)
        self.assertIn("Alice", result)

    def test_to_toml_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_toml(schema=UserSchema)


class io_dict_to_xml_schema_test_case(unittest.TestCase):
    def test_to_xml_with_schema_valid(self) -> None:
        d = benedict({"root": {"name": "Alice", "age": 30}})
        result = d.to_xml(schema=XMLWrappedSchema)
        self.assertIsInstance(result, str)
        self.assertIn("Alice", result)
        self.assertIn("30", result)

    def test_to_xml_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"root": {"name": "Alice", "age": 30, "email": "alice@example.com"}})
        result = d.to_xml(schema=XMLWrappedSchema)
        self.assertNotIn("email", result)
        self.assertIn("Alice", result)

    def test_to_xml_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"root": {"name": "Alice"}})  # root.age required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_xml(schema=XMLWrappedSchema)


class io_dict_to_base64_schema_test_case(unittest.TestCase):
    def test_to_base64_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_base64(schema=UserSchema)
        decoded = IODict.from_base64(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})

    def test_to_base64_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_base64(schema=UserSchema)
        decoded = IODict.from_base64(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})
        self.assertNotIn("email", decoded)

    def test_to_base64_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_base64(schema=UserSchema)


class io_dict_to_pickle_schema_test_case(unittest.TestCase):
    def test_to_pickle_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_pickle(schema=UserSchema)
        decoded = IODict.from_pickle(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})

    def test_to_pickle_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_pickle(schema=UserSchema)
        decoded = IODict.from_pickle(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})
        self.assertNotIn("email", decoded)

    def test_to_pickle_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_pickle(schema=UserSchema)


class io_dict_to_plist_schema_test_case(unittest.TestCase):
    def test_to_plist_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_plist(schema=UserSchema)
        decoded = IODict.from_plist(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})

    def test_to_plist_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_plist(schema=UserSchema)
        decoded = IODict.from_plist(result)
        self.assertEqual(dict(decoded), {"name": "Alice", "age": 30})
        self.assertNotIn("email", decoded)

    def test_to_plist_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_plist(schema=UserSchema)


class io_dict_to_query_string_schema_test_case(unittest.TestCase):
    def test_to_query_string_with_schema_valid(self) -> None:
        d = benedict({"name": "Alice", "age": 30})
        result = d.to_query_string(schema=UserSchema)
        self.assertIsInstance(result, str)
        self.assertIn("Alice", result)

    def test_to_query_string_with_schema_strips_extra_fields(self) -> None:
        d = benedict({"name": "Alice", "age": 30, "email": "alice@example.com"})
        result = d.to_query_string(schema=UserSchema)
        self.assertNotIn("email", result)
        self.assertIn("Alice", result)

    def test_to_query_string_with_schema_missing_required_field_raises(self) -> None:
        d = benedict({"name": "Alice"})  # 'age' required
        with self.assertRaises((pydantic.ValidationError, ValueError)):
            d.to_query_string(schema=UserSchema)
