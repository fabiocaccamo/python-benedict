import unittest
from unittest.mock import patch

from pydantic import BaseModel, ValidationError

from benedict.exceptions import ExtrasRequireModuleNotFoundError
from benedict.utils import pydantic_util


class User(BaseModel):
    name: str
    age: int


class TestPydanticUtil(unittest.TestCase):
    def setUp(self):
        self.valid_data = {"name": "John", "age": 30}
        self.invalid_data = {"name": "John", "age": "not_an_int"}

    def test_validate_data_with_valid_data(self):
        # validation with valid data succeeds
        validated = pydantic_util.validate_data(self.valid_data, schema=User)
        self.assertEqual(validated["name"], "John")
        self.assertEqual(validated["age"], 30)

    def test_validate_data_with_invalid_data(self):
        # validation with invalid data raises ValidationError
        with self.assertRaises(ValidationError):
            pydantic_util.validate_data(self.invalid_data, schema=User)

    def test_validate_data_with_no_schema(self):
        # validation without schema returns original data
        data = {"any": "data"}
        validated = pydantic_util.validate_data(data, schema=None)
        self.assertEqual(validated, data)

    def test_validate_data_with_invalid_schema(self):
        # validation with non-pydantic schema raises ValueError
        class NotAModel:
            pass

        with self.assertRaises(ValueError) as cm:
            pydantic_util.validate_data(self.valid_data, schema=NotAModel)
        self.assertEqual(
            str(cm.exception), "Invalid schema. Schema must be a Pydantic model class."
        )

        # validation with invalid schema type raises ValueError
        with self.assertRaises(ValueError) as cm:
            pydantic_util.validate_data(self.valid_data, schema="not_a_schema")
        self.assertEqual(
            str(cm.exception), "Invalid schema. Schema must be a Pydantic model class."
        )

    @patch("benedict.utils.pydantic_util.pydantic_installed", False)
    @patch("benedict.utils.pydantic_util.BaseModel", None)
    def test_validate_data_when_pydantic_not_installed(self):
        # validation without schema still works when pydantic is not installed
        data = {"any": "data"}
        validated = pydantic_util.validate_data(data, schema=None)
        self.assertEqual(validated, data)

        # validation with schema raises ExtrasRequireModuleNotFoundError
        with self.assertRaises(ExtrasRequireModuleNotFoundError):
            pydantic_util.validate_data(self.valid_data, schema=User)
