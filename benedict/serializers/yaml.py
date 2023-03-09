try:
    import yaml

    # fix benedict yaml representer - #43
    from yaml import SafeDumper
    from yaml.representer import SafeRepresenter

    yaml_installed = True
except ModuleNotFoundError:
    yaml_installed = False


from benedict.extras import require_yaml
from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.json import JSONSerializer


class YAMLSerializer(AbstractSerializer):
    """
    This class describes an yaml serializer.
    """

    @staticmethod
    def represent_dict_for_class(cls):
        if yaml_installed:
            # fix benedict yaml representer - #43
            SafeDumper.yaml_representers[cls] = SafeRepresenter.represent_dict

    def __init__(self):
        super().__init__(
            extensions=[
                "yaml",
                "yml",
            ],
        )
        self._json_serializer = JSONSerializer()

    def decode(self, s, **kwargs):
        require_yaml(installed=yaml_installed)
        data = yaml.safe_load(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        require_yaml(installed=yaml_installed)
        d = self._json_serializer.decode(self._json_serializer.encode(d))
        data = yaml.dump(d, **kwargs)
        return data
