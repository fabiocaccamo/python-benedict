# -*- coding: utf-8 -*-

from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict.dicts.utility import UtilityDict


def benediction(method):
    def wrapper(*args, **kwargs):
        value = method(*args, **kwargs)
        value_benedicted = benedict.cast(value)
        return value_benedicted if value_benedicted is not None else value
    return wrapper


class benedict(KeypathDict, ParseDict, UtilityDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    @benediction
    def copy(self):
        return super(benedict, self).copy()

    @benediction
    def deepcopy(self):
        return super(benedict, self).deepcopy()

    @classmethod
    @benediction
    def fromkeys(cls, sequence, value=None):
        return KeypathDict.fromkeys(sequence, value)

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
        values = [(benedict.cast(value) or value) for value in values]
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

