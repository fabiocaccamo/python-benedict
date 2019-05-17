# -*- coding: utf-8 -*-

from benedict import parser
from decimal import Decimal
from six import string_types

__all__ = ['benedict', 'KeypathDict', 'UtilityDict']


class KeypathDict(dict):

    def __init__(self, *args, **kwargs):
        super(KeypathDict, self).__init__(*args, **kwargs)

    def _join_keys(self, keys):
        return '.'.join(keys)

    def _split_keys(self, key):
        if isinstance(key, string_types):
            keypath = key
            separator = '.'
            if separator in keypath:
                keys = list(keypath.split(separator))
                keys_count = len(keys)
                return keys
            else:
                return [key]
        else:
            return [key]

    def _get_value_by_keys(self, keys, default=None):
        i = 0
        j = len(keys)
        item = self
        while i < j:
            key = keys[i]
            # if key not in item:
            #    return default
            try:
                item = item[key]
                if item is None:
                    return default
            except KeyError as key_error:
                return default
            i += 1
        return (item if item != None else default)

    def _set_value_by_keys(self, keys, value):
        i = 0
        j = len(keys)
        item = self
        while i < j:
            key = keys[i]
            if i < (j - 1):
                subitem = item.get(key, None)
                if not isinstance(subitem, dict):
                    subitem = item[key] = {}
                item = subitem
            else:
                item[key] = value
            i += 1

    def __contains__(self, key):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_keys = keys[:-1]
            item_key = keys[-1]
            item_parent = self.get(self._join_keys(item_keys), None)
            if isinstance(item_parent, dict):
                if item_key in item_parent:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return super(KeypathDict, self).__contains__(key)

    def __delitem__(self, key):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_keys = keys[:-1]
            item_key = keys[-1]
            item_parent = self.get(self._join_keys(item_keys), None)
            if isinstance(item_parent, dict):
                if item_key in item_parent:
                    del item_parent[item_key]
        else:
            try:
                super(KeypathDict, self).__delitem__(key)
            except KeyError as error:
                pass

    def __getitem__(self, key):
        keys = self._split_keys(key)
        value = None
        if len(keys) > 1:
            value = self._get_value_by_keys(keys)
        else:
            try:
                value = super(KeypathDict, self).__getitem__(key)
            except KeyError as error:
                value = None
        return value

    def __setitem__(self, key, value):
        keys = self._split_keys(key)
        if len(keys) > 1:
            self._set_value_by_keys(keys, value)
        else:
            super(KeypathDict, self).__setitem__(key, value)

    def get(self, key, default=None):
        keys = self._split_keys(key)
        if len(keys) > 1:
            return self._get_value_by_keys(keys, default)
        else:
            return super(KeypathDict, self).get(key, default)

    def set(self, key, value):
        self[key] = value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
            return default
        else:
            return self[key]


class UtilityDict(dict):

    def __init__(self, *args, **kwargs):
        super(UtilityDict, self).__init__(*args, **kwargs)

    def get_bool(self, key, default=False):
        """
        Get value by key or keypath trying to return it as bool.
        Values like `1`, `true`, `yes`, `on` will be returned as `True`.
        """
        return self.get_value(
            key, default, [True, False], parser.parse_bool)

    def get_bool_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_bool)

    def get_datetime(self, key, default=None, format=None, options=[]):
        """
        Get value by key or keypath trying to return it as datetime.
        If format is not specified it will be autodetected.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_datetime, {'format': format})

    def get_datetime_list(self, key, default=[], format=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of datetime values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_datetime, {'format': format})

    def get_decimal(self, key, default=Decimal('0.0'), options=[]):
        """
        Get value by key or keypath trying to return it as Decimal.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_decimal)

    def get_decimal_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of Decimal values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_decimal)

    def get_dict(self, key, default={}):
        """
        Get value by key or keypath trying to return it as dict.
        If value is a json string it will be automatically decoded.
        """
        return self.get_value(
            key, default, None, parser.parse_dict)

    def get_float(self, key, default=0.0, options=[]):
        """
        Get value by key or keypath trying to return it as float.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_float)

    def get_float_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of float values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_float)

    def get_int(self, key, default=0, options=[]):
        """
        Get value by key or keypath trying to return it as int.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_int)

    def get_int_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of int values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_int)

    def get_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_value(
            key, default, None, parser.parse_list, {'separator': separator})

    def get_slug(self, key, default='', options=[]):
        """
        Get value by key or keypath trying to return it as slug.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_slug)

    def get_slug_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of slug values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_slug)

    def get_str(self, key, default='', options=[]):
        """
        Get value by key or keypath trying to return it as string.
        Encoding issues will be automatically fixed.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_str)

    def get_str_list(self, key, default=[], separator=','):
        """
        Get value by key or keypath trying to return it as list of str values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_str)

    def get_value(self, key, default=None, options=[],
                  parser_func=lambda val: val, parser_kwargs={}):
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
        if parser_func and callable(parser_func):
            value = parser_func(self.get(key, ''), **parser_kwargs)
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

    def get_values_list(self, key, default=[], separator=',',
                       parser_func=lambda val: val, parser_kwargs={}):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        values_list = self.get_list(key, None, separator)
        if values_list is None:
            return default
        else:
            return [parser_func(value, **parser_kwargs) for value in values_list]


class benedict(KeypathDict, UtilityDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

