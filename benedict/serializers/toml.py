try:
    import toml

    toml_installed = True
except ModuleNotFoundError:
    toml_installed = False

try:
    # python >= 3.11
    import tomllib

    tomllib_available = True
except ImportError:
    tomllib_available = False

from benedict.extras import require_toml
from benedict.serializers.abstract import AbstractSerializer


class TOMLSerializer(AbstractSerializer):
    """
    This class describes a toml serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "toml",
            ],
        )

    def decode(self, s, **kwargs):
        if tomllib_available:
            data = tomllib.loads(s, **kwargs)
        else:
            require_toml(installed=toml_installed)
            data = toml.loads(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        require_toml(installed=toml_installed)
        data = toml.dumps(dict(d), **kwargs)
        return data
