# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

from six import text_type

import json


class JSONSerializer(AbstractSerializer):

    def __init__(self):
        super(JSONSerializer, self).__init__()

    def decode(self, s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        kwargs.setdefault('default', self._encode_default)
        data = json.dumps(d, **kwargs)
        return data

    def _encode_default(self, obj):
        if type_util.is_set(obj):
            return list(obj)
        elif type_util.is_datetime(obj):
            return obj.isoformat()
        elif type_util.is_decimal(obj):
            return text_type(obj)
        return text_type(obj)
