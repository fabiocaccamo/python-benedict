# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import toml


class TOMLSerializer(AbstractSerializer):

    def __init__(self):
        super(TOMLSerializer, self).__init__()

    def decode(self, s, **kwargs):
        data = toml.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = toml.dumps(d, **kwargs)
        return data
