from typing import Any

import xmltodict

from benedict.serializers.abstract import AbstractSerializer


class XMLSerializer(AbstractSerializer):
    """
    This class describes a xml serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "xml",
            ],
        )

    def decode(self, s: str, **kwargs: Any):
        kwargs.setdefault("dict_constructor", dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def encode(self, d, **kwargs: Any):
        data = xmltodict.unparse(d, **kwargs)
        return data
