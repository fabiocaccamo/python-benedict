# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict.dicts.utility import UtilityDict


def benediction(method):
    def wrapper(*args, **kwargs):
        value = method(*args, **kwargs)
        return benedict.cast(value)
    return wrapper


class benedict(IODict, KeypathDict, ParseDict, UtilityDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    @classmethod
    def cast(cls, value):
        if isinstance(value, dict) and not isinstance(value, cls):
            return cls(value)
        else:
            return value

    @benediction
    def clone(self):
        return super(benedict, self).clone()

    @benediction
    def copy(self):
        return super(benedict, self).copy()

    @benediction
    def deepcopy(self):
        return super(benedict, self).deepcopy()

    @benediction
    def filter(self, predicate):
        return super(benedict, self).filter(predicate)

    @benediction
    def flatten(self, separator='_'):
        return super(benedict, self).flatten(separator)

    @classmethod
    @benediction
    def fromkeys(cls, sequence, value=None):
        return KeypathDict.fromkeys(sequence, value)

    # @staticmethod
    # @benediction
    # def from_base64(s, **kwargs):
    #     return IODict.from_base64(s, **kwargs)

    @staticmethod
    @benediction
    def from_json(s, **kwargs):
        return IODict.from_json(s, **kwargs)

    # @staticmethod
    # @benediction
    # def from_query_string(s, **kwargs):
    #     return IODict.from_query_string(s, **kwargs)

    @staticmethod
    @benediction
    def from_toml(s, **kwargs):
        return IODict.from_toml(s, **kwargs)

    @staticmethod
    @benediction
    def from_xml(s, **kwargs):
        return IODict.from_xml(s, **kwargs)

    @staticmethod
    @benediction
    def from_yaml(s, **kwargs):
        return IODict.from_yaml(s, **kwargs)

    @benediction
    def __getitem__(self, key):
        return super(benedict, self).__getitem__(key)

    @benediction
    def get(self, key, default=None):
        return super(benedict, self).get(key, default)

    @benediction
    def get_dict(self, key, default=None):
        return super(benedict, self).get_dict(key, default)

    def get_list(self, key, default=None, separator=','):
        values = super(benedict, self).get_list(key, default, separator)
        values = [benedict.cast(value) for value in values]
        return values

    @benediction
    def get_list_item(self, key, index=0, default=None, separator=','):
        return super(benedict, self).get_list_item(
            key, index, default, separator)

    @benediction
    def get_phonenumber(self, key, country_code=None, default=''):
        return super(benedict, self).get_phonenumber(
            key, country_code, default)

    @benediction
    def pop(self, key, default=None):
        return super(benedict, self).pop(key, default)

    @benediction
    def setdefault(self, key, default=None):
        return super(benedict, self).setdefault(key, default)

    @benediction
    def subset(self, keys):
        return super(benedict, self).subset(keys)
