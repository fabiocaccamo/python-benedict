# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.json import JSONSerializer

import yaml


class YAMLSerializer(AbstractSerializer):
    """
    This class describes an yaml serializer.
    """

    def __init__(self):
        super(YAMLSerializer, self).__init__(
            extensions=[
                "yaml",
                "yml",
            ],
        )
        self._json_serializer = JSONSerializer()

    def decode(self, s, **kwargs):
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        d = self._json_serializer.decode(self._json_serializer.encode(d))
        data = yaml.dump(d, **kwargs)
        return data
