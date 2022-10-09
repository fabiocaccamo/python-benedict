# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

import json


class JSONSerializer(AbstractSerializer):
    """
    This class describes a json serializer.
    """

    def __init__(self):
        super(JSONSerializer, self).__init__(
            extensions=[
                "json",
            ],
        )

    def decode(self, s, **kwargs):
        data = json.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        kwargs.setdefault("default", self._encode_default)
        data = json.dumps(d, **kwargs)
        return data

    def _encode_default(self, obj):
        if type_util.is_set(obj):
            return list(obj)
        elif type_util.is_datetime(obj):
            return obj.isoformat()
        elif type_util.is_decimal(obj):
            return str(obj)
        return str(obj)
