import toml

try:
    # python >= 3.11
    import tomllib

    tomllib_available = True
except ImportError:
    tomllib_available = False

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
        if tomllib_available:
            data = tomllib.loads(s, **kwargs)
        else:
            data = toml.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = toml.dumps(dict(d), **kwargs)
        return data
