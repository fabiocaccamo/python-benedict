import tomllib

try:
    import tomli_w

    tomli_w_installed = True
except ModuleNotFoundError:  # pragma: no cover
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
        data = tomllib.loads(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        require_toml(installed=tomli_w_installed)
        result: str = tomli_w.dumps(dict(d), **kwargs)
        return result
