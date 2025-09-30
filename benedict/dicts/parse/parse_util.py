from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal, DecimalException

try:
    import ftfy
    import phonenumbers
    from dateutil import parser as date_parser
    from MailChecker import MailChecker
    from phonenumbers import PhoneNumberFormat, phonenumberutil

    parse_installed = True
except ModuleNotFoundError:
    parse_installed = False


from collections.abc import Callable
from typing import Any, cast

from slugify import slugify
from typing_extensions import TypeIs, overload

from benedict.extras import require_parse
from benedict.serializers import JSONSerializer
from benedict.utils import type_util

CallableIsBool = Callable[[Any], TypeIs[bool]]
CallableIsDecimal = Callable[[Any], TypeIs[Decimal]]
CallableIsDict = Callable[[Any], TypeIs[dict[str, Any]]]
CallableIsListOrTuple = Callable[[Any], TypeIs[list[Any] | tuple[Any, ...]]]
CallableIsFloat = Callable[[Any], TypeIs[float]]
CallableIsInt = Callable[[Any], TypeIs[int]]
CallableIsStr = Callable[[Any], TypeIs[str]]

ParseWithTypeChecker = (
    CallableIsBool
    | CallableIsDecimal
    | CallableIsDict
    | CallableIsFloat
    | CallableIsInt
    | CallableIsListOrTuple
    | CallableIsStr
)
ParseWithParser = (
    Callable[..., bool | None]
    | Callable[..., Decimal | None]
    | Callable[..., dict[str, Any] | None]
    | Callable[..., float | None]
    | Callable[..., int | None]
    | Callable[..., list[Any] | tuple[Any, ...] | None]
    | Callable[..., str | None]
)
ParseWithInputOutput = (
    bool | Decimal | float | dict[str, Any] | list[Any] | str | tuple[Any, ...] | None
)


@overload
def _parse_with(
    val: bool | str,
    type_checker: CallableIsBool | None,
    parser: Callable[..., bool | None],
    **kwargs: Any,
) -> bool | None: ...


@overload
def _parse_with(
    val: Decimal | str,
    type_checker: CallableIsDecimal | None,
    parser: Callable[..., Decimal | None],
    **kwargs: Any,
) -> Decimal | None: ...


@overload
def _parse_with(
    val: str | dict[str, Any],
    type_checker: CallableIsDict | None,
    parser: Callable[..., dict[str, Any] | None],
    **kwargs: Any,
) -> dict[str, Any] | None: ...


@overload
def _parse_with(
    val: int | str,
    type_checker: CallableIsInt | None,
    parser: Callable[..., int | None],
    **kwargs: Any,
) -> int | None: ...


@overload
def _parse_with(
    val: float | str,
    type_checker: CallableIsFloat | None,
    parser: Callable[..., float | None],
    **kwargs: Any,
) -> float | None: ...


@overload
def _parse_with(
    val: list[Any] | tuple[Any, ...] | str,
    type_checker: CallableIsListOrTuple | None,
    parser: Callable[..., list[Any] | tuple[Any, ...] | None],
    **kwargs: Any,
) -> list[Any] | tuple[Any, ...] | None: ...


@overload
def _parse_with(
    val: str,
    type_checker: CallableIsStr | None,
    parser: Callable[..., str | None],
    **kwargs: Any,
) -> str | None: ...


def _parse_with(  # type: ignore[misc]
    val: ParseWithInputOutput,
    type_checker: ParseWithTypeChecker,
    parser: ParseWithParser,
    **kwargs: Any,
) -> ParseWithInputOutput:
    if val is None:
        return None
    if callable(type_checker) and type_checker(val):
        return val
    s = str(val)
    if not len(s):
        return None
    return parser(s, **kwargs)


def _parse_bool(val: str) -> bool | None:
    val = val.lower()
    if val in ["1", "true", "yes", "ok", "on"]:
        return True
    elif val in ["0", "false", "no", "ko", "off"]:
        return False
    return None


def parse_bool(val: Any) -> bool | None:
    return _parse_with(val, type_util.is_bool, _parse_bool)


def parse_date(val: str | datetime, format: str | None = None) -> date | None:
    v = parse_datetime(val, format)
    if v:
        return v.date()
    return None


def _parse_datetime_with_format(val: str, format: str | None) -> datetime | None:
    try:
        return datetime.strptime(val, format or "")
    except Exception:
        return None


def _parse_datetime_without_format(val: str) -> datetime | None:
    try:
        return date_parser.parse(val)
    except Exception:
        return _parse_datetime_from_timestamp(val)


def _parse_datetime_from_timestamp(val: str | int | float) -> datetime | None:
    try:
        return datetime.fromtimestamp(float(val))
    except Exception:
        return None


def parse_datetime(val: str | datetime, format: str | None = None) -> datetime | None:
    require_parse(installed=parse_installed)
    if type_util.is_datetime(val):
        return val
    s = str(val)
    if format:
        return _parse_datetime_with_format(s, format)
    else:
        return _parse_datetime_without_format(s)


def _parse_decimal(val: str) -> Decimal | None:
    try:
        return Decimal(val)
    except (ValueError, DecimalException):
        return None


def parse_decimal(val: str) -> Decimal | None:
    return _parse_with(val, type_util.is_decimal, _parse_decimal)


def _parse_dict(val: str) -> dict[Any, Any] | None:
    serializer = JSONSerializer()
    try:
        d = serializer.decode(val)
        if type_util.is_dict(d):
            return d
        return None
    except Exception:
        return None


def parse_dict(val: str | dict[str, Any]) -> dict[Any, Any] | None:
    return _parse_with(val, type_util.is_dict, _parse_dict)


def _parse_float(val: str) -> float | None:
    try:
        return float(val)
    except ValueError:
        return None


def parse_float(val: str) -> float | None:
    return _parse_with(val, type_util.is_float, _parse_float)


def _parse_email(val: str, check_blacklist: bool = True) -> str | None:
    val = val.lower()
    if check_blacklist:
        if not MailChecker.is_valid(val):
            return None
    else:
        if not MailChecker.is_valid_email_format(val):
            return None
    return val


def parse_email(val: str, check_blacklist: bool = True) -> str | None:
    require_parse(installed=parse_installed)
    return _parse_with(val, None, _parse_email, check_blacklist=check_blacklist)


def _parse_int(val: str) -> int | None:
    try:
        return int(val)
    except ValueError:
        return None


def parse_int(val: int | str) -> int | None:
    return _parse_with(val, type_util.is_integer, _parse_int)


def _parse_list(val: str, separator: str | None = None) -> list[Any] | None:
    if (
        val.startswith("{")
        and val.endswith("}")
        or val.startswith("[")
        and val.endswith("]")
    ):
        try:
            serializer = JSONSerializer()
            ls: list[Any] | None = serializer.decode(val)
            if type_util.is_list(ls):
                return ls
            return None
        except Exception:
            pass
    if separator:
        ls = list(val.split(separator))
        return ls
    return None


def parse_list(
    val: str | tuple[Any, ...] | list[Any], separator: str | None = None
) -> list[Any] | None:
    v = _parse_with(val, type_util.is_list_or_tuple, _parse_list, separator=separator)
    if type_util.is_list_or_tuple(v):
        return list(v)
    return v  # type: ignore[return-value]


def _parse_phonenumber(
    val: str, country_code: str | None = None
) -> dict[str, str] | None:
    try:
        phone_obj = phonenumbers.parse(val, country_code)
        if phonenumbers.is_valid_number(phone_obj):
            return {
                "e164": phonenumbers.format_number(phone_obj, PhoneNumberFormat.E164),
                "international": phonenumbers.format_number(
                    phone_obj, PhoneNumberFormat.INTERNATIONAL
                ),
                "national": phonenumbers.format_number(
                    phone_obj, PhoneNumberFormat.NATIONAL
                ),
            }
        return None
    except phonenumberutil.NumberParseException:
        return None


def parse_phonenumber(
    val: str, country_code: str | None = None
) -> dict[str, str] | None:
    require_parse(installed=parse_installed)
    s = parse_str(val)
    if not s:
        return None
    phone_raw = re.sub(r"[^0-9\+]", " ", s)
    phone_raw = phone_raw.strip()
    if phone_raw.startswith("00"):
        phone_raw = "+" + phone_raw[2:]
    if country_code and len(country_code) >= 2:
        country_code = country_code[0:2].upper()
    return _parse_with(phone_raw, None, _parse_phonenumber, country_code=country_code)


def _parse_slug(val: str) -> str:
    result: str = slugify(val)
    return result


def parse_slug(val: Any) -> str:
    s = parse_str(val)
    return _parse_slug(s)


def parse_str(val: Any) -> str:
    require_parse(installed=parse_installed)
    if type_util.is_string(val):
        val = ftfy.fix_text(val)
    else:
        val = str(val)
    val = val.strip()
    val = " ".join(val.split())
    return cast("str", val)


def parse_uuid(val: str) -> str | None:
    s = parse_str(val)
    return s if type_util.is_uuid(s) else None
