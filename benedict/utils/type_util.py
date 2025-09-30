from __future__ import annotations

import pathlib
import re
from collections.abc import Callable, Collection, Sequence
from datetime import datetime
from decimal import Decimal
from typing import Any

from typing_extensions import TypeIs

regex = re.compile("").__class__
uuid_re = re.compile(
    "^([0-9a-f]{32}){1}$|^([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}){1}$",
    flags=re.IGNORECASE,
)


def is_bool(val: Any) -> TypeIs[bool]:
    return isinstance(val, bool)


def is_collection(val: Any) -> TypeIs[Collection[Any]]:
    return isinstance(val, (dict, list, set, tuple))


def is_datetime(val: Any) -> TypeIs[datetime]:
    return isinstance(val, datetime)


def is_decimal(val: Any) -> TypeIs[Decimal]:
    return isinstance(val, Decimal)


def is_dict(val: Any) -> TypeIs[dict[Any, Any]]:
    return isinstance(val, dict)


def is_dict_or_list(val: Any) -> TypeIs[dict[Any, Any] | list[Any]]:
    return isinstance(val, (dict, list))


def is_dict_or_list_or_tuple(
    val: Any,
) -> TypeIs[dict[Any, Any] | list[Any] | tuple[Any]]:
    return isinstance(val, (dict, list, tuple))


def is_float(val: Any) -> TypeIs[float]:
    return isinstance(val, float)


def is_function(val: Any) -> TypeIs[Callable[..., Any]]:
    return callable(val)


def is_integer(val: Any) -> TypeIs[int]:
    return isinstance(val, int)


def is_json_serializable(
    val: Any,
) -> TypeIs[bool | dict[Any, Any] | float | int | list[Any] | str | tuple[Any] | None]:
    json_types = (type(None), bool, dict, float, int, list, str, tuple)
    return isinstance(val, json_types)


def is_list(val: Any) -> TypeIs[list[Any]]:
    return isinstance(val, list)


def is_sequence(val: Any) -> TypeIs[Sequence[Any]]:
    return isinstance(val, Sequence)


def is_list_or_tuple(val: Any) -> TypeIs[list[Any] | tuple[Any]]:
    return isinstance(val, (list, tuple))


def is_none(val: Any) -> TypeIs[None]:
    return val is None


def is_not_none(val: Any) -> bool:
    return val is not None


def is_path(val: Any) -> TypeIs[pathlib.Path]:
    return isinstance(val, pathlib.Path)


def is_regex(val: Any) -> TypeIs[re.Pattern[Any]]:
    return isinstance(val, regex)


def is_set(val: Any) -> TypeIs[set[Any]]:
    return isinstance(val, set)


def is_string(val: Any) -> TypeIs[str]:
    return isinstance(val, str)


def is_tuple(val: Any) -> TypeIs[tuple[Any]]:
    return isinstance(val, tuple)


def is_uuid(val: Any) -> bool:
    return bool(is_string(val) and uuid_re.match(val))
