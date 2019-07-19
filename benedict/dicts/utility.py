# -*- coding: utf-8 -*-

from six import string_types

import copy
import json


class UtilityDict(dict):

    def __init__(self, *args, **kwargs):
        super(UtilityDict, self).__init__(*args, **kwargs)

    @classmethod
    def cast(cls, value):
        if isinstance(value, dict) and not isinstance(value, cls):
            return cls(value)
        else:
            return None

    def clean(self, strings=True, dicts=True, lists=True):
        keys = list(self.keys())
        for key in keys:
            value = self.get(key, None)
            if not value:
                if value is None or \
                        strings and isinstance(value, string_types) or \
                        dicts and isinstance(value, dict) or \
                        lists and isinstance(value, (list, tuple, )):
                    del self[key]

    def deepcopy(self):
        return copy.deepcopy(self)

    @staticmethod
    def dump(data):
        def encoder(obj):
            json_types = (bool, dict, float, int, list, tuple, ) + string_types
            if not isinstance(obj, json_types):
                return str(obj)
        return json.dumps(data, indent=4, sort_keys=True, default=encoder)

    def dump_items(self, key=None):
        return self.dump(self.get(key) if key else self)

    def filter(self, predicate):
        if not callable(predicate):
            raise ValueError('predicate argument must be a callable.')
        d = {}
        keys = self.keys()
        for key in keys:
            val = self.get(key, None)
            if predicate(key, val):
                d[key] = val
        return d

    def remove(self, keys):
        for key in keys:
            try:
                del self[key]
            except KeyError:
                continue
            # print('REMOVE', key)
            # self.pop(key, 1)

    def subset(self, keys):
        d = self.__class__()
        for key in keys:
            d[key] = self.get(key, None)
        return d
