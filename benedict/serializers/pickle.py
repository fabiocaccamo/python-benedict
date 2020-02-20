# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import pickle


class PickleSerializer(AbstractSerializer):

    def __init__(self):
        super(PickleSerializer, self).__init__()

    def decode(self, b, **kwargs):
        data = pickle.loads(b, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = pickle.dumps(d, **kwargs)
        return data
