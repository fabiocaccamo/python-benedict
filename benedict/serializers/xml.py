# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import xmltodict


class XMLSerializer(AbstractSerializer):

    @staticmethod
    def decode(s, **kwargs):
        kwargs.setdefault('dict_constructor', dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    @staticmethod
    def encode(d, **kwargs):
        data = xmltodict.unparse(d, **kwargs)
        return data
