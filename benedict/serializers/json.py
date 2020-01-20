# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import json


class JSONSerializer(AbstractSerializer):

    def __init__(self):
        super(JSONSerializer, self).__init__()

    def decode(self, s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = json.dumps(d, **kwargs)
        return data
