# -*- coding: utf-8 -*-

from benedict.dicts.keypath import KeypathDict
from benedict.dicts.parse import ParseDict

from copy import deepcopy


class benedict(KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def copy(self):
        return benedict(
            super(benedict, self).copy())

    def deepcopy(self):
        return benedict(
            deepcopy(self))

    @classmethod
    def fromkeys(cls, sequence, value=None):
        return benedict(
            KeypathDict.fromkeys(sequence, value))

