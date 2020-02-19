# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import toml


class TOMLSerializer(AbstractSerializer):

    @staticmethod
    def decode(s, **kwargs):
        data = toml.loads(s, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        data = toml.dumps(d, **kwargs)
        return data
