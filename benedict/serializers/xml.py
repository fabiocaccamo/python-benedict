# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer

import xmltodict


class XMLSerializer(AbstractSerializer):
    """
    This class describes a xml serializer.
    """

    def __init__(self):
        super(XMLSerializer, self).__init__(
            extensions=[
                "xml",
            ],
        )

    def decode(self, s, **kwargs):
        kwargs.setdefault("dict_constructor", dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = xmltodict.unparse(d, **kwargs)
        return data
