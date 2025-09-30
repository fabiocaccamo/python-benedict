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

from typing import Any

from benedict.extras import require_toml
from benedict.serializers.abstract import AbstractSerializer


class TOMLSerializer(AbstractSerializer[str, Any]):
    """
    This class describes a toml serializer.
    """

    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "toml",
            ],
        )

    def decode(self, s: str, **kwargs: Any) -> Any:
        if tomllib_available:
            data = tomllib.loads(s, **kwargs)
        else:
            require_toml(installed=toml_installed)
            data = toml.loads(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        require_toml(installed=toml_installed)
        data = toml.dumps(dict(d), **kwargs)
        return data
