# -*- coding: utf-8 -*-

from benedict import parser
from copy import deepcopy
from decimal import Decimal
from six import string_types

__all__ = ['benedict', 'KeypathDict', 'UtilityDict']


class KeypathDict(dict):

    def __init__(self, *args, **kwargs):
        super(KeypathDict, self).__init__(*args, **kwargs)

    @classmethod
    def _join_keys(cls, keys):
        return '.'.join(keys)

    @classmethod
    def _split_keys(cls, key):
        if isinstance(key, string_types):
            keypath = key
            separator = '.'
            if separator in keypath:
                keys = list(keypath.split(separator))
                return keys
            else:
                return [key]
        else:
            return [key]

    def _get_value_by_keys(self, keys):
        i = 0
        j = len(keys)
        val = self
        while i < j:
            key = keys[i]
            try:
                val = val[key]
            except KeyError:
                val = None
                break
            i += 1
        return val

    def _get_value_context_by_keys(self, keys):
        item_keys = keys[:-1]
        item_key = keys[-1]
        item_parent = self._get_value_by_keys(item_keys)
        return (item_parent, item_key, )

    def _has_value_by_keys(self, keys):
        item_parent, item_key = self._get_value_context_by_keys(keys)
        if isinstance(item_parent, dict):
            if item_key in item_parent:
                return True
            else:
                return False
        else:
            return False

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
            return self._has_value_by_keys(keys)
        else:
            return super(KeypathDict, self).__contains__(key)

    def __delitem__(self, key):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                del item_parent[item_key]
            else:
                raise KeyError
        else:
            super(KeypathDict, self).__delitem__(key)

    def __getitem__(self, key):
        keys = self._split_keys(key)
        value = None
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent[item_key]
            else:
                raise KeyError
        else:
            value = super(KeypathDict, self).__getitem__(key)
        return value

    def __setitem__(self, key, value):
        keys = self._split_keys(key)
        if len(keys) > 1:
            self._set_value_by_keys(keys, value)
        else:
            super(KeypathDict, self).__setitem__(key, value)

    def copy(self):
        return KeypathDict(
            super(KeypathDict, self).copy())

    def deepcopy(self):
        return KeypathDict(deepcopy(self))

    def fromkeys(sequence, value=None):
        d = KeypathDict()
        for key in sequence:
            d[key] = value
        return d

    def get(self, key, default=None):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                return item_parent.get(item_key, default)
            else:
                return default
        else:
            return super(KeypathDict, self).get(key, default)

    def get_keypaths(self):
        def walk_keypaths(root, path):
            keypaths = []
            for key, val in root.items():
                keypaths += [self._join_keys(path + [key])]
                if isinstance(val, dict):
                    keypaths += walk_keypaths(val, path + [key])
            return keypaths
        keypaths = walk_keypaths(self, [])
        keypaths.sort()
        return keypaths

    def pop(self, key, default=None):
        keys = self._split_keys(key)
        if len(keys) > 1:
            item_parent, item_key = self._get_value_context_by_keys(keys)
            if isinstance(item_parent, dict):
                if default is None:
                    return item_parent.pop(item_key)
                else:
                    return item_parent.pop(item_key, default)
            else:
                if default is None:
                    raise KeyError
                else:
                    return default
        else:
            if default is None:
                return super(KeypathDict, self).pop(key)
            else:
                return super(KeypathDict, self).pop(key, default)

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

    def get_bool_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_bool)

    def get_datetime(self, key, default=None, format=None, options=None):
        """
        Get value by key or keypath trying to return it as datetime.
        If format is not specified it will be autodetected.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_datetime,
            {'format': format})

    def get_datetime_list(self, key, default=None, format=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of datetime values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_datetime,
            {'format': format})

    def get_decimal(self, key, default=Decimal('0.0'), options=None):
        """
        Get value by key or keypath trying to return it as Decimal.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_decimal)

    def get_decimal_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of Decimal values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_decimal)

    def get_dict(self, key, default=None):
        """
        Get value by key or keypath trying to return it as dict.
        If value is a json string it will be automatically decoded.
        """
        return self.get_value(
            key, default or {}, None, parser.parse_dict)

    def get_float(self, key, default=0.0, options=None):
        """
        Get value by key or keypath trying to return it as float.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_float)

    def get_float_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of float values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_float)

    def get_int(self, key, default=0, options=None):
        """
        Get value by key or keypath trying to return it as int.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_int)

    def get_int_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of int values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_int)

    def get_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_value(
            key, default or [], None, parser.parse_list,
            {'separator': separator})

    def get_slug(self, key, default='', options=None):
        """
        Get value by key or keypath trying to return it as slug.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_slug)

    def get_slug_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of slug values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_slug)

    def get_str(self, key, default='', options=None):
        """
        Get value by key or keypath trying to return it as string.
        Encoding issues will be automatically fixed.
        If options and value is in options return value otherwise default.
        """
        return self.get_value(
            key, default, options, parser.parse_str)

    def get_str_list(self, key, default=None, separator=','):
        """
        Get value by key or keypath trying to return it as list of str values.
        If separator is specified and value is a string it will be splitted.
        """
        return self.get_values_list(
            key, default, separator, parser.parse_str)

    def get_value(self, key, default=None, options=None,
                  parser_func=lambda val: val, parser_kwargs=None):
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
            value = parser_func(self.get(key, ''), **(parser_kwargs or {}))
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

    def get_values_list(self, key, default=None, separator=',',
                        parser_func=lambda val: val, parser_kwargs=None):
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        if key not in self:
            return default or []
        values_list = self.get_list(key, [], separator)
        return [parser_func(value, **(parser_kwargs or {}))
                for value in values_list]


class benedict(KeypathDict, UtilityDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def copy(self):
        return benedict(
            super(benedict, self).copy())

    def deepcopy(self):
        return benedict(
            super(benedict, self).deepcopy())

    def fromkeys(sequence, value=None):
        return benedict(
            KeypathDict.fromkeys(sequence, value))

