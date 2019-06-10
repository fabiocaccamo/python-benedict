# -*- coding: utf-8 -*-

from benedict.dicts.keypath import KeypathDict
# from benedict.dicts.io import IODict
from benedict.dicts.parse import ParseDict

import copy


class benedict(KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        attr = super(benedict, self).__getattribute__(name)
        if hasattr(attr, '__call__'):
            def attr_wrapper(*args, **kwargs):
                value = attr(*args, **kwargs)
                if name.startswith('_'):
                    return value
                else:
                    return benedict._cast(value)
            return attr_wrapper
        else:
            return attr

    def __getitem__(self, key):
        return benedict._cast(
            super(benedict, self).__getitem__(key))

    @staticmethod
    def _cast(value):
        if isinstance(value, dict) and not isinstance(value, benedict):
            return benedict(value)
        else:
            return value

    def deepcopy(self):
        return copy.deepcopy(self)

    @classmethod
    def fromkeys(cls, sequence, value=None):
        return benedict._cast(
            KeypathDict.fromkeys(sequence, value))

