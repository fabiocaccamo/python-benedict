# -*- coding: utf-8 -*-

import toml

from benedict.serializers.abstract import AbstractSerializer


class TOMLSerializer(AbstractSerializer):
    """
    This class describes a toml serializer.
    """

    def __init__(self):
        super(TOMLSerializer, self).__init__(
            extensions=[
                "toml",
            ],
        )

    def decode(self, s, **kwargs):
        data = toml.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = toml.dumps(dict(d), **kwargs)
        return data
