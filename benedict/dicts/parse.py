# -*- coding: utf-8 -*-

from benedict.utils import parse_util

from decimal import Decimal


class ParseDict(dict):

    def __init__(self, *args, **kwargs):
        super(ParseDict, self).__init__(*args, **kwargs)

    def _get_value(self, key, default, options,
                   parser_func, parser_kwargs=None):
        """
        Get value by key or keypath core method.
        If options and value is in options return value otherwise default.
        """
        # Get raw value from self.
        value = self.get(key, None)
        # If value is None return default value.
        if value is None:
            return default

        # If not of the desired type, try to parse it using parser_func.
        value = parser_func(value, **(parser_kwargs or {}))
        # If value is None after parsing return default value.
        if value is None:
            return default

        # If options and value in options return value otherwise default.
        if isinstance(options, (list, tuple, )) and len(options):
            if value in options:
                return value
            else:
                return default
        else:
            return value

    def _get_values_list(self, key, default, separator,
                         parser_func, parser_kwargs=None):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        if key not in self:
            return default or []
        values_list = self.get_list(key, [], separator)
        return [parser_func(value, **(parser_kwargs or {}))
                for value in values_list]

    def get_bool(self, key, default=False):
        """
        Get value by key or keypath trying to return it as bool.
        Values like `1`, `true`, `yes`, `on` will be returned as `True`.
        """
        return self._get_value(
            key, default, [True, False], parse_util.parse_bool)

    def get_bool_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_bool)

    def get_datetime(self, key, default=None, format=None, options=None):
        """
        Get value by key or keypath trying to return it as datetime.
        If format is not specified it will be autodetected.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_datetime,
            {'format': format})

    def get_datetime_list(self, key, default=None, format=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of datetime values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_datetime,
            {'format': format})

    def get_decimal(self, key, default=Decimal('0.0'), options=None):
        """
        Get value by key or keypath trying to return it as Decimal.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_decimal)

    def get_decimal_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of Decimal values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_decimal)

    def get_dict(self, key, default=None):
        """
        Get value by key or keypath trying to return it as dict.
        If value is a json string it will be automatically decoded.
        """
        return self._get_value(
            key, default or {}, None, parse_util.parse_dict)

    def get_email(self, key, default='', options=None, check_blacklist=True):
        """
        Get email by key or keypath and return it.
        If value is blacklisted it will be automatically ignored.
        If check_blacklist is False, it will be not ignored even if blacklisted.
        """
        return self._get_value(
            key, default, options, parse_util.parse_email,
            {'check_blacklist': check_blacklist})

    def get_float(self, key, default=0.0, options=None):
        """
        Get value by key or keypath trying to return it as float.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_float)

    def get_float_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of float values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_float)

    def get_int(self, key, default=0, options=None):
        """
        Get value by key or keypath trying to return it as int.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_int)

    def get_int_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of int values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_int)

    def get_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_value(
            key, default or [], None, parse_util.parse_list,
            {'separator': separator})

    def get_list_item(self, key, index=0, default=None, separator=','):
        """
        Get list by key or keypath and return value at the specified index.
        If separator is specified and list value is a string it will be splitted.
        """
        values = self.get_list(key, None, separator)
        if values:
            try:
                value = values[index]
                return value
            except IndexError:
                return default
        else:
            return default

    def get_phonenumber(self, key, country_code=None, default=None):
        """
        Get phone number by key or keypath and return a dict with different formats (e164, international, national).
        If country code is specified (alpha 2 code), it will be used to parse phone number correctly.
        """
        return self._get_value(
            key, default or {}, None, parse_util.parse_phonenumber,
            {'country_code': country_code})

    def get_slug(self, key, default='', options=None):
        """
        Get value by key or keypath trying to return it as slug.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_slug)

    def get_slug_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of slug values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_slug)

    def get_str(self, key, default='', options=None):
        """
        Get value by key or keypath trying to return it as string.
        Encoding issues will be automatically fixed.
        If options and value is in options return value otherwise default.
        """
        return self._get_value(
            key, default, options, parse_util.parse_str)

    def get_str_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of str values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_str)
