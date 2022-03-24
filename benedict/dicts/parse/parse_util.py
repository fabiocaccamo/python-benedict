# -*- coding: utf-8 -*-

from benedict.serializers import JSONSerializer
from benedict.utils import type_util

from datetime import datetime
from dateutil import parser as date_parser
from decimal import Decimal, DecimalException
from MailChecker import MailChecker
from phonenumbers import phonenumberutil, PhoneNumberFormat
from slugify import slugify

import ftfy
import phonenumbers
import re


def _parse_with(val, type_checker, parser, **kwargs):
    if val is None:
        return None
    if callable(type_checker) and type_checker(val):
        return val
    s = str(val)
    if not len(s):
        return None
    return parser(s, **kwargs)


def _parse_bool(val):
    val = val.lower()
    if val in ["1", "true", "yes", "ok", "on"]:
        return True
    elif val in ["0", "false", "no", "ko", "off"]:
        return False
    return None


def parse_bool(val):
    return _parse_with(val, type_util.is_bool, _parse_bool)


def parse_date(val, format=None):
    val = parse_datetime(val, format)
    if val:
        return val.date()
    return None


def _parse_datetime_with_format(val, format):
    try:
        return datetime.strptime(val, format)
    except Exception:
        return None


def _parse_datetime_without_format(val):
    try:
        return date_parser.parse(val)
    except Exception:
        return _parse_datetime_from_timestamp(val)


def _parse_datetime_from_timestamp(val):
    try:
        return datetime.fromtimestamp(float(val))
    except Exception:
        return None


def parse_datetime(val, format=None):
    if type_util.is_datetime(val):
        return val
    s = str(val)
    if format:
        return _parse_datetime_with_format(s, format)
    else:
        return _parse_datetime_without_format(s)


def _parse_decimal(val):
    try:
        return Decimal(val)
    except (ValueError, DecimalException):
        return None


def parse_decimal(val):
    return _parse_with(val, type_util.is_decimal, _parse_decimal)


def _parse_dict(val):
    serializer = JSONSerializer()
    try:
        d = serializer.decode(val)
        if type_util.is_dict(d):
            return d
        return None
    except Exception:
        return None


def parse_dict(val):
    return _parse_with(val, type_util.is_dict, _parse_dict)


def _parse_float(val):
    try:
        return float(val)
    except ValueError:
        return None


def parse_float(val):
    return _parse_with(val, type_util.is_float, _parse_float)


def _parse_email(val, check_blacklist=True):
    val = val.lower()
    if check_blacklist:
        if not MailChecker.is_valid(val):
            return None
    else:
        if not MailChecker.is_valid_email_format(val):
            return None
    return val


def parse_email(val, check_blacklist=True):
    return _parse_with(val, None, _parse_email, check_blacklist=check_blacklist)


def _parse_int(val):
    try:
        return int(val)
    except ValueError:
        return None


def parse_int(val):
    return _parse_with(val, type_util.is_integer, _parse_int)


def _parse_list(val, separator=None):
    if (
        val.startswith("{")
        and val.endswith("}")
        or val.startswith("[")
        and val.endswith("]")
    ):
        try:
            serializer = JSONSerializer()
            ls = serializer.decode(val)
            if type_util.is_list(ls):
                return ls
            return None
        except Exception:
            pass
    if separator:
        ls = list(val.split(separator))
        return ls
    return None


def parse_list(val, separator=None):
    val = _parse_with(val, type_util.is_list_or_tuple, _parse_list, separator=separator)
    return list(val) if type_util.is_list_or_tuple(val) else val


def _parse_phonenumber(val, country_code=None):
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


def parse_phonenumber(val, country_code=None):
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


def _parse_slug(val):
    return slugify(val)


def parse_slug(val):
    s = parse_str(val)
    return _parse_slug(s)


def parse_str(val):
    if type_util.is_string(val):
        val = ftfy.fix_text(val)
    else:
        val = str(val)
    val = val.strip()
    val = " ".join(val.split())
    return val


def parse_uuid(val):
    s = parse_str(val)
    return s if type_util.is_uuid(s) else None
