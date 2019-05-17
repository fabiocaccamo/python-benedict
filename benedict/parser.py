# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import parser as date_parser
from decimal import Decimal, DecimalException
from slugify import slugify

import ftfy
import json
# import xmltodict
# import yaml


def parse_bool(val):
    if isinstance(val, bool):
        return val
    str_val = str(val).lower()
    val = None
    if str_val in ['1', 'true', 'yes', 'on']:
        val = True
    elif str_val in ['0', 'false', 'no', 'off']:
        val = False
    return val


def parse_datetime(val, format=None):
    if isinstance(val, datetime):
        return val
    str_val = str(val)
    val = None
    try:
        if format:
            val = datetime.strptime(str_val, format)
        else:
            val = date_parser.parse(str_val)
    except Exception as datetime_error:
        pass
    return val


def parse_decimal(val):
    if isinstance(val, Decimal):
        return val
    str_val = str(val)
    val = None
    try:
        val = Decimal(str_val)
    except (ValueError, DecimalException) as decimal_error:
        pass
    return val


def parse_dict(val):
    if isinstance(val, dict):
        return val
    str_val = str(val)
    if not len(str_val):
        return None
    val = None
    try:
        val = json.loads(str_val)
        if not isinstance(val, dict):
            val = None
    except Exception as json_error:
        # try:
        #     val = yaml.safe_load(str_val)
        # except yaml.YAMLError as yaml_error:
        #     try:
        #         val = xmltodict.parse(str_val)
        #     except Exception as xml_error:
        #         pass
        pass
    return val


def parse_float(val):
    if isinstance(val, float):
        return val
    str_val = str(val)
    val = None
    try:
        val = float(str_val)
    except ValueError as float_error:
        pass
    return val


def parse_int(val):
    if isinstance(val, int):
        return val
    str_val = str(val)
    val = None
    try:
        val = int(str_val)
    except ValueError as int_error:
        pass
    return val


def parse_list(val, separator=None):
    if isinstance(val, (list, tuple, )):
        return list(val)
    str_val = str(val)
    if not len(str_val):
        return None
    val = None
    try:
        val = json.loads(str_val)
        if not isinstance(val, list):
            val = None
    except Exception as json_error:
        if separator:
            val = list(str_val.split(separator))
    return val


def parse_slug(val):
    return slugify(ftfy.fix_text(str(val)))


def parse_str(val):
    return ftfy.fix_text(str(val))

