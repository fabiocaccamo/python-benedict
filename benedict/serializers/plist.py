# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer

import plistlib


class PListSerializer(AbstractSerializer):
    """
    This class describes a p list serializer.
    https://docs.python.org/3/library/plistlib.html
    """

    def __init__(self):
        super(PListSerializer, self).__init__(
            extensions=[
                "plist",
            ],
        )

    def decode(self, s, **kwargs):
        kwargs.setdefault("fmt", plistlib.FMT_XML)
        encoding = kwargs.pop("encoding", "utf-8")
        return plistlib.loads(s.encode(encoding), **kwargs)

    def encode(self, d, **kwargs):
        encoding = kwargs.pop("encoding", "utf-8")
        return plistlib.dumps(d, **kwargs).decode(encoding)
