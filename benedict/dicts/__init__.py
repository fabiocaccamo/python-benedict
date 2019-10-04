# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict.utils import dict_util


def benediction(method):
    def wrapper(*args, **kwargs):
        value = method(*args, **kwargs)
        if isinstance(value, dict) and not isinstance(value, benedict):
            return benedict(value)
        return value
    return wrapper


class benedict(IODict, KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def clean(self, strings=True, dicts=True, lists=True):
        dict_util.clean(self, strings=strings, dicts=dicts, lists=lists)

    @benediction
    def clone(self):
        return dict_util.clone(self)

    @benediction
    def copy(self):
        return super(benedict, self).copy()

    def deepcopy(self):
        return self.clone()

    def deepupdate(self, other, *args):
        self.merge(other, *args)

    def dump(self, data=None):
        return dict_util.dump(data or self)

    @benediction
    def filter(self, predicate):
        return dict_util.filter(self, predicate)

    @benediction
    def flatten(self, separator='_'):
        return dict_util.flatten(self, separator)

    @classmethod
    @benediction
    def fromkeys(cls, sequence, value=None):
        return KeypathDict.fromkeys(sequence, value)

    @staticmethod
    @benediction
    def from_base64(s, **kwargs):
        return IODict.from_base64(s, **kwargs)

    @staticmethod
    @benediction
    def from_json(s, **kwargs):
        return IODict.from_json(s, **kwargs)

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
    def invert(self, flat=False):
        return dict_util.invert(self, flat)

    def items_sorted_by_keys(self, reverse=False):
        return dict_util.items_sorted_by_keys(self, reverse=reverse)

    def items_sorted_by_values(self, reverse=False):
        return dict_util.items_sorted_by_values(self, reverse=reverse)

    def merge(self, other, *args):
        dicts = [other] + list(args)
        for d in dicts:
            dict_util.merge(self, d)

    def remove(self, keys, *args):
        if isinstance(keys, string_types):
            keys = [keys]
        keys += args
        for key in keys:
            try:
                del self[key]
            except KeyError:
                continue

    @benediction
    def subset(self, keys):
        d = self.__class__()
        for key in keys:
            d[key] = self.get(key, None)
        return d
