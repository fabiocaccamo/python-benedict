from typing import Any

from benedict.extras import require_validate

try:
    from pydantic import BaseModel

    pydantic_installed = True
except ModuleNotFoundError:
    pydantic_installed = False
    BaseModel = None

PydanticModel = type["BaseModel"]


def _is_pydantic_model(obj: Any) -> bool:
    """
    Check if an object is a Pydantic model class.
    """
    return (
        pydantic_installed
        and BaseModel is not None
        and isinstance(obj, type)
        and issubclass(obj, BaseModel)
    )


def validate_data(data: Any, *, schema: PydanticModel | None = None) -> Any:
    """
    Validate data against a Pydantic schema if provided.
    """
    if schema is None:
        return data

    require_validate(installed=pydantic_installed)

    if not _is_pydantic_model(schema):
        raise ValueError("Invalid schema. Schema must be a Pydantic model class.")

    validated = schema.model_validate(data)
    return validated.model_dump()
