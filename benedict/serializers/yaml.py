try:
    import yaml

    # fix benedict yaml representer - #43
    from yaml import SafeDumper
    from yaml.representer import SafeRepresenter

    yaml_installed = True
except ModuleNotFoundError:
    yaml_installed = False


from typing import Any, cast

from benedict.extras import require_yaml
from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.json import JSONSerializer


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
        self._json_serializer = JSONSerializer()

    def decode(self, s: str, **kwargs: Any) -> Any:
        require_yaml(installed=yaml_installed)
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d: Any, **kwargs: Any) -> str:
        require_yaml(installed=yaml_installed)
        d = self._json_serializer.decode(self._json_serializer.encode(d))
        data = yaml.dump(d, **kwargs)
        return cast("str", data)
