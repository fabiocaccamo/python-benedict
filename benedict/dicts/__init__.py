# -*- coding: utf-8 -*-

from benedict.dicts.io import IODict
from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict
from benedict.utils import dict_util


class benedict(IODict, KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def clean(self, strings=True, dicts=True, lists=True):
        dict_util.clean(self, strings=strings, dicts=dicts, lists=lists)

    def clone(self):
        return dict_util.clone(self)

    def copy(self):
        return benedict(super(benedict, self).copy())

    def deepcopy(self):
        return self.clone()

    def deepupdate(self, other, *args):
        self.merge(other, *args)

    def dump(self, data=None):
        return dict_util.dump(data or self)

    def filter(self, predicate):
        return dict_util.filter(self, predicate)

    def flatten(self, separator='_'):
        return dict_util.flatten(self, separator)

    def invert(self, flat=False):
        return dict_util.invert(self, flat)

    def items_sorted_by_keys(self, reverse=False):
        return dict_util.items_sorted_by_keys(self, reverse=reverse)

    def items_sorted_by_values(self, reverse=False):
        return dict_util.items_sorted_by_values(self, reverse=reverse)

    def keypaths(self):
        sep = self._keypath_separator or '.'
        return dict_util.keypaths(self, separator=sep)

    def merge(self, other, *args):
        dict_util.merge(self, other, *args)

    def move(self, key_src, key_dest):
        dict_util.move(self, key_src, key_dest)

    def remove(self, keys, *args):
        dict_util.remove(self, keys, *args)

    def standardize(self):
        dict_util.standardize(self)

    def subset(self, keys, *args):
        return dict_util.subset(self, keys, *args)

    def swap(self, key1, key2):
        dict_util.swap(self, key1, key2)

    def traverse(self, callback):
        dict_util.traverse(self, callback)

    def unique(self):
        dict_util.unique(self)
