# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import json


class JSONSerializer(AbstractSerializer):

    @staticmethod
    def decode(s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        data = json.dumps(d, **kwargs)
        return data
