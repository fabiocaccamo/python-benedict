import unittest

from pydantic import BaseModel, ValidationError

from benedict.dicts.io import IODict


class TestIODictValidate(unittest.TestCase):
    def setUp(self):
        class User(BaseModel):
            name: str
            age: int
            email: str

        class UserOptional(BaseModel):
            name: str
            age: int | None = None
            email: str | None = None

        self.User = User
        self.UserOptional = UserOptional
        self.valid_data = {
            "name": "John",
            "age": 30,
            "email": "john@example.com",
        }
        self.invalid_data = {
            "name": "John",
            "age": "not_an_int",
            "email": "john@example.com",
        }
        self.minimal_data = {"name": "John"}
        self.data_with_extra_fields = {
            "name": "John",
            "age": 30,
            "email": "john@example.com",
            "role": "admin",
            "active": True,
        }

    def test_validate_valid_data(self):
        d = IODict(self.valid_data)
        d.validate(schema=self.User)
        self.assertEqual(d["name"], "John")
        self.assertEqual(d["age"], 30)
        self.assertEqual(d["email"], "john@example.com")

    def test_validate_invalid_data(self):
        d = IODict(self.invalid_data)
        with self.assertRaises(ValidationError):
            d.validate(schema=self.User)

    def test_validate_optional_fields(self):
        d = IODict(self.minimal_data)
        d.validate(schema=self.UserOptional)
        self.assertEqual(d["name"], "John")
        self.assertIsNone(d.get("age"))
        self.assertIsNone(d.get("email"))

    def test_validate_removes_extra_fields(self):
        d = IODict(self.data_with_extra_fields)
        d.validate(schema=self.User)
        # required fields are preserved
        self.assertEqual(d["name"], "John")
        self.assertEqual(d["age"], 30)
        self.assertEqual(d["email"], "john@example.com")
        # extra fields are removed
        self.assertNotIn("role", d)
        self.assertNotIn("active", d)
        # only the schema fields exist
        self.assertEqual(set(d.keys()), {"name", "age", "email"})

    def test_validate_invalid_schema(self):
        class InvalidSchema:
            pass

        d = IODict(self.valid_data)
        with self.assertRaises(ValueError):
            d.validate(schema=InvalidSchema)

        with self.assertRaises(ValueError):
            d.validate(schema="not_a_schema")
