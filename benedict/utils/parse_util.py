# -*- coding: utf-8 -*-

from benedict.utils import type_util

from datetime import datetime
from dateutil import parser as date_parser
from decimal import Decimal, DecimalException
from MailChecker import MailChecker
from phonenumbers import phonenumberutil, PhoneNumberFormat
from six import text_type
from slugify import slugify

import ftfy
import json
import phonenumbers
import re


def parse_bool(val):
    if type_util.is_bool(val):
        return val
    str_val = text_type(val).lower()
    if str_val in ['1', 'true', 'yes', 'ok', 'on']:
        return True
    elif str_val in ['0', 'false', 'no', 'ko', 'off']:
        return False
    return None


def parse_datetime(val, format=None):
    if type_util.is_datetime(val):
        return val
    str_val = text_type(val)
    if format:
        try:
            val = datetime.strptime(str_val, format)
            return val
        except Exception:
            return None
    try:
        val = date_parser.parse(str_val)
        return val
    except Exception:
        try:
            val = datetime.fromtimestamp(float(str_val))
            return val
        except Exception:
            return None


def parse_decimal(val):
    if type_util.is_decimal(val):
        return val
    str_val = text_type(val)
    try:
        val = Decimal(str_val)
        return val
    except (ValueError, DecimalException):
        return None


def parse_dict(val):
    if type_util.is_dict(val):
        return val
    str_val = text_type(val)
    if not len(str_val):
        return None
    try:
        val = json.loads(str_val)
        if type_util.is_dict(val):
            return val
        return None
    except Exception:
        return None


def parse_float(val):
    if type_util.is_float(val):
        return val
    str_val = text_type(val)
    try:
        val = float(str_val)
        return val
    except ValueError:
        return None


def parse_email(val, check_blacklist=True):
    val = parse_str(val)
    if not val:
        return None
    val = val.lower()
    if check_blacklist:
        if not MailChecker.is_valid(val):
            return None
    else:
        if not MailChecker.is_valid_email_format(val):
            return None
    return val


def parse_int(val):
    if type_util.is_integer(val):
        return val
    str_val = text_type(val)
    try:
        val = int(str_val)
        return val
    except ValueError:
        return None


def parse_list(val, separator=None):
    if type_util.is_list_or_tuple(val):
        return list(val)
    str_val = text_type(val)
    if not len(str_val):
        return None
    try:
        val = json.loads(str_val)
        if type_util.is_list(val):
            return val
        return None
    except Exception:
        if separator:
            val = list(str_val.split(separator))
            return val
        return None


def parse_phonenumber(val, country_code=None):
    val = parse_str(val)
    if not val:
        return None
    phone_raw = re.sub(r'[^0-9\+]', ' ', val)
    phone_raw = phone_raw.strip()
    if phone_raw.startswith('00'):
        phone_raw = '+{}'.format(phone_raw[2:])
    phone_country_code = None
    if country_code and len(country_code) >= 2:
        phone_country_code = country_code[0:2].upper()
    try:
        phone_obj = phonenumbers.parse(phone_raw, phone_country_code)
        if phonenumbers.is_valid_number(phone_obj):
            return {
                'e164': phonenumbers.format_number(
                    phone_obj, PhoneNumberFormat.E164),
                'international': phonenumbers.format_number(
                    phone_obj, PhoneNumberFormat.INTERNATIONAL),
                'national': phonenumbers.format_number(
                    phone_obj, PhoneNumberFormat.NATIONAL),
            }
        return None
    except phonenumberutil.NumberParseException:
        return None


def parse_slug(val):
    return slugify(parse_str(val))


def parse_str(val):
    if type_util.is_string(val):
        try:
            val = ftfy.fix_text(val)
        except UnicodeError:
            pass
    else:
        val = text_type(val)
    val = val.strip()
    val = ' '.join(val.split())
    return val
