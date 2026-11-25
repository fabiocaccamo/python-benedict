from __future__ import annotations

try:
    import yaml

    # fix benedict yaml representer - #43
    from yaml import SafeDumper
    from yaml.representer import SafeRepresenter

    yaml_installed = True
except ModuleNotFoundError:  # pragma: no cover
    yaml_installed = False


from datetime import date, datetime
from typing import Any, cast

from benedict.extras import require_yaml
from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

# values yaml can represent natively without losing their type.
_YAML_NATIVE_TYPES: tuple[type, ...] = (
    type(None),
    bool,
    float,
    int,
    str,
    date,
    datetime,
)


class YAMLSerializer(AbstractSerializer[str, Any]):
    """
    This class describes an yaml serializer.
    """

    @staticmethod
    def represent_dict_for_class(cls: Any) -> None:
        if yaml_installed:
            # fix benedict yaml representer - #43
            SafeDumper.yaml_representers[cls] = SafeRepresenter.represent_dict  # type: ignore[assignment]

    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "yaml",
                "yml",
            ],
        )

    def decode(self, s: str, **kwargs: Any) -> Any:
        require_yaml(installed=yaml_installed)
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        require_yaml(installed=yaml_installed)
        data = yaml.safe_dump(self._encode_data(d), **kwargs)
        return cast("str", data)

    def _encode_key(self, key: Any) -> Any:
        if isinstance(key, (bool, float, int, str)) or key is None:
            # keep keys that yaml can represent natively
            return key
        return str(key)

    def _encode_data(self, data: Any, ancestors: set[int] | None = None) -> Any:
        if ancestors is None:
            ancestors = set()
        if type_util.is_dict(data):
            if id(data) in ancestors:
                raise ValueError("Circular reference detected.")
            ancestors.add(id(data))
            try:
                return {
                    self._encode_key(key): self._encode_data(value, ancestors)
                    for key, value in data.items()
                }
            finally:
                ancestors.discard(id(data))
        if type_util.is_list_or_tuple(data) or type_util.is_set(data):
            return [self._encode_data(value, ancestors) for value in data]
        if isinstance(data, (date, datetime)):
            # yaml supports dates/timestamps natively
            return data
        if type_util.is_decimal(data):
            return str(data)
        if isinstance(data, _YAML_NATIVE_TYPES):
            return data
        return str(data)
