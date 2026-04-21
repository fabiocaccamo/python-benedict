try:
    # python >= 3.11
    import tomllib

    tomllib_available = True
except ImportError:
    tomllib_available = False

try:
    import tomli

    tomli_installed = True
except ModuleNotFoundError:
    tomli_installed = False

try:
    import tomli_w

    tomli_w_installed = True
except ModuleNotFoundError:
    tomli_w_installed = False

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
            require_toml(installed=tomli_installed)
            data = tomli.loads(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        require_toml(installed=tomli_w_installed)
        data = tomli_w.dumps(dict(d), **kwargs)
        return data
