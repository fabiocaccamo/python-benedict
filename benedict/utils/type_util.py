import pathlib
import re
from datetime import datetime
from decimal import Decimal
from typing import Any

regex = re.compile("").__class__
uuid_re = re.compile(
    "^([0-9a-f]{32}){1}$|^([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}){1}$",
    flags=re.IGNORECASE,
)


def is_bool(val: Any) -> bool:
    return isinstance(val, bool)


def is_collection(val: Any) -> bool:
    return isinstance(val, (dict, list, set, tuple))


def is_datetime(val: Any) -> bool:
    return isinstance(val, datetime)


def is_decimal(val: Any) -> bool:
    return isinstance(val, Decimal)


def is_dict(val: Any) -> bool:
    return isinstance(val, dict)


def is_dict_or_list(val: Any) -> bool:
    return isinstance(val, (dict, list))


def is_dict_or_list_or_tuple(val: Any) -> bool:
    return isinstance(val, (dict, list, tuple))


def is_float(val: Any) -> bool:
    return isinstance(val, float)


def is_function(val: Any) -> bool:
    return callable(val)


def is_integer(val: Any) -> bool:
    return isinstance(val, int)


def is_json_serializable(val: Any) -> bool:
    json_types = (type(None), bool, dict, float, int, list, str, tuple)
    return isinstance(val, json_types)


def is_list(val: Any) -> bool:
    return isinstance(val, list)


def is_list_or_tuple(val: Any) -> bool:
    return isinstance(val, (list, tuple))


def is_none(val: Any) -> bool:
    return val is None


def is_not_none(val: Any) -> bool:
    return val is not None


def is_path(val: Any) -> bool:
    return isinstance(val, pathlib.Path)


def is_regex(val: Any) -> bool:
    return isinstance(val, regex)


def is_set(val: Any) -> bool:
    return isinstance(val, set)


def is_string(val: Any) -> bool:
    return isinstance(val, str)


def is_tuple(val: Any) -> bool:
    return isinstance(val, tuple)


def is_uuid(val: Any) -> bool:
    return is_string(val) and bool(uuid_re.match(val))
