# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import pickle


class PickleSerializer(AbstractSerializer):

    @staticmethod
    def decode(b, **kwargs):
        data = pickle.loads(b, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        data = pickle.dumps(d, **kwargs)
        return data
