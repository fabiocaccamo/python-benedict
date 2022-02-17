# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer

import yaml


class YAMLSerializer(AbstractSerializer):
    """
    This class describes an yaml serializer.
    """

    def __init__(self):
        super(YAMLSerializer, self).__init__()

    def decode(self, s, **kwargs):
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = yaml.dump(dict(d.items()), **kwargs)
        return data
