# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

from six import text_type

import json


class JSONSerializer(AbstractSerializer):

    @staticmethod
    def decode(s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        kwargs.setdefault('default', JSONSerializer._encode_default)
        data = json.dumps(d, **kwargs)
        return data

    @staticmethod
    def _encode_default(obj):
        if type_util.is_json_serializable(obj):
            return None
        elif type_util.is_set(obj):
            return list(obj)
        elif type_util.is_datetime(obj):
            return obj.isoformat()
        elif type_util.is_decimal(obj):
            return text_type(obj)
        return text_type(obj)
