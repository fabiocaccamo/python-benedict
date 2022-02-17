# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal

import re

regex = re.compile("").__class__
uuid_re = re.compile(
    "^([0-9a-f]{32}){1}$|^([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}){1}$",
    flags=re.IGNORECASE,
)


def is_bool(val):
    return isinstance(val, bool)


def is_collection(val):
    return isinstance(val, (dict, list, set, tuple))


def is_datetime(val):
    return isinstance(val, datetime)


def is_decimal(val):
    return isinstance(val, Decimal)


def is_dict(val):
    return isinstance(val, dict)


def is_dict_or_list(val):
    return isinstance(val, (dict, list))


def is_dict_or_list_or_tuple(val):
    return isinstance(val, (dict, list, tuple))


def is_float(val):
    return isinstance(val, float)


def is_function(val):
    return callable(val)


def is_integer(val):
    return isinstance(val, int)


def is_json_serializable(val):
    json_types = (type(None), bool, dict, float, int, list, str, tuple)
    return isinstance(val, json_types)


def is_list(val):
    return isinstance(val, list)


def is_list_or_tuple(val):
    return isinstance(val, (list, tuple))


def is_none(val):
    return val is None


def is_not_none(val):
    return val is not None


def is_regex(val):
    return isinstance(val, regex)


def is_set(val):
    return isinstance(val, set)


def is_string(val):
    return isinstance(val, str)


def is_tuple(val):
    return isinstance(val, tuple)


def is_uuid(val):
    return is_string(val) and uuid_re.match(val)
