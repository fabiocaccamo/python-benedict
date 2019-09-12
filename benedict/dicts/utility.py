# -*- coding: utf-8 -*-

from benedict.utils import utility_util


class UtilityDict(dict):

    def __init__(self, *args, **kwargs):
        super(UtilityDict, self).__init__(*args, **kwargs)

    def clean(self, strings=True, dicts=True, lists=True):
        utility_util.clean(self, strings=strings, dicts=dicts, lists=lists)

    def clone(self):
        return utility_util.clone(self)

    def deepcopy(self):
        return self.clone()

    def deepupdate(self, other, *args):
        self.merge(other, *args)

    def dump(self, data=None):
        return utility_util.dump(data or self)

    def filter(self, predicate):
        if not callable(predicate):
            raise ValueError('predicate argument must be a callable.')
        return utility_util.filter(self, predicate)

    def flatten(self, separator='_'):
        return utility_util.flatten(self, separator)

    def merge(self, other, *args):
        dicts = [other] + list(args)
        for d in dicts:
            utility_util.merge(self, d)

    def remove(self, keys):
        for key in keys:
            try:
                del self[key]
            except KeyError:
                continue

    def subset(self, keys):
        d = self.__class__()
        for key in keys:
            d[key] = self.get(key, None)
        return d
