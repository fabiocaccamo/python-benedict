# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import yaml


class YAMLSerializer(AbstractSerializer):

    @staticmethod
    def decode(s, **kwargs):
        data = yaml.safe_load(s, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        data = yaml.dump(dict(d), **kwargs)
        return data
