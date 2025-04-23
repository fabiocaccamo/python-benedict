import json
import unittest

from pydantic import BaseModel, ValidationError

from benedict import benedict


class TestIODictSchema(unittest.TestCase):
    def setUp(self):
        class User(BaseModel):
            name: str
            age: int
            email: str

        class UserList(BaseModel):
            users: list[User]

        class UserOptional(BaseModel):
            name: str
            age: int | None = None
            email: str | None = None

        self.User = User
        self.UserList = UserList
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

    def test_constructor_with_schema(self):
        d = benedict(self.valid_data, schema=self.User)
        self.assertEqual(d["name"], "John")
        self.assertEqual(d["age"], 30)
        self.assertEqual(d["email"], "john@example.com")

        with self.assertRaises(ValidationError):
            benedict(self.invalid_data, schema=self.User)

    def test_constructor_with_schema_and_optional_fields(self):
        d = benedict(self.minimal_data, schema=self.UserOptional)
        self.assertEqual(d["name"], "John")
        self.assertIsNone(d.get("age"))
        self.assertIsNone(d.get("email"))

    def test_constructor_with_invalid_schema(self):
        class InvalidSchema:
            pass

        with self.assertRaises(ValueError):
            benedict(self.valid_data, schema=InvalidSchema)

        with self.assertRaises(ValueError):
            benedict(self.valid_data, schema="not_a_schema")

    def test_from_json_with_schema_and_valid_data(self):
        json_data = json.dumps(self.valid_data)
        d = benedict.from_json(json_data, schema=self.User)
        self.assertEqual(d["name"], "John")
        self.assertEqual(d["age"], 30)

    def test_from_json_with_schema_and_invalid_data(self):
        json_data = json.dumps(self.invalid_data)
        with self.assertRaises(ValidationError):
            benedict.from_json(json_data, schema=self.User)


if __name__ == "__main__":
    unittest.main()
