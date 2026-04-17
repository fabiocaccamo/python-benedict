from __future__ import annotations

from typing import Any

try:
    import pydantic

    pydantic_installed = True
except ModuleNotFoundError:
    pydantic_installed = False


def apply_schema(data: Any, schema: Any) -> Any:
    """
    Validate and parse data using a Pydantic model class.
    Returns the validated data as a plain dict.
    Raises ExtrasRequireModuleNotFoundError if pydantic is not installed.
    """
    from benedict.extras import require_schema

    require_schema(installed=pydantic_installed)
    instance = schema.model_validate(data)
    return instance.model_dump()
