from __future__ import annotations

from typing import Any

try:
    import pydantic

    pydantic_installed = True
except ImportError:  # pragma: no cover
    pydantic_installed = False


def apply_schema(data: Any, schema: Any) -> Any:
    """
    Validate and parse data using a Pydantic model class.
    Returns the validated data as a plain dict.
    Raises ExtrasRequireModuleNotFoundError if pydantic is not installed.
    Raises TypeError if schema is not a pydantic BaseModel subclass.
    """
    from benedict.extras import require_schema

    require_schema(installed=pydantic_installed)
    if isinstance(schema, type) and issubclass(schema, pydantic.BaseModel):
        schema_cls: type[pydantic.BaseModel] = schema
    else:
        raise TypeError(
            f"schema must be a pydantic BaseModel subclass, got {type(schema)!r}"
        )
    instance = schema_cls.model_validate(data)
    return instance.model_dump()
