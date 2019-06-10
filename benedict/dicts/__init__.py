# -*- coding: utf-8 -*-

from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict

from copy import deepcopy


class benedict(KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    @staticmethod
    def cast(val):
        if isinstance(val, dict) and not isinstance(val, benedict):
            return benedict(val)
        else:
            return val

    def copy(self):
        return benedict.cast(
            super(benedict, self).copy())

    def deepcopy(self):
        return benedict.cast(
            deepcopy(self))

    @classmethod
    def fromkeys(cls, sequence, value=None):
        return benedict.cast(
            KeypathDict.fromkeys(sequence, value))

    def __getitem__(self, key):
        return benedict.cast(
            super(benedict, self).__getitem__(key))

    def get(self, key, default=None):
        return benedict.cast(
            super(benedict, self).get(key, default))

    def pop(self, key, default=None):
        return benedict.cast(
            super(benedict, self).pop(key, default))

    def setdefault(self, key, default=None):
        return benedict.cast(
            super(benedict, self).setdefault(key, default))

