# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import xmltodict


class XMLSerializer(AbstractSerializer):

    def __init__(self):
        super(XMLSerializer, self).__init__()

    def decode(self, s, **kwargs):
        kwargs.setdefault('dict_constructor', dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = xmltodict.unparse(d, **kwargs)
        return data
