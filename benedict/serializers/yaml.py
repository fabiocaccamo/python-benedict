from typing import Any

import yaml

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.json import JSONSerializer


class YAMLSerializer(AbstractSerializer):
    """
    This class describes an yaml serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "yaml",
                "yml",
            ],
        )
        self._json_serializer = JSONSerializer()

    def decode(self, s: str, **kwargs: Any):
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d, **kwargs: Any) -> str:
        d = self._json_serializer.decode(self._json_serializer.encode(d))
        data = yaml.dump(d, **kwargs)
        return data
