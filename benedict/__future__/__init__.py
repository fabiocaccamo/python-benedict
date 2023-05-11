import json

from benedict.dicts import benedict as _benedict
from benedict.serializers import YAMLSerializer


class benedict(_benedict):
    def to_ini(self, **kwargs):
        def super_class(*vargs):
            return self.__class__.__bases__[0](*vargs)

        data = {}

        for section, keys in self.dict().items():
            data[section] = {}
            for key, value in keys.items():
                data[section][key] = json.dumps(value)

        return super_class(data).to_ini(**kwargs)

    @classmethod
    def from_ini(cls, s, **kwargs):
        ini = super().from_ini(s, **kwargs)

        data = {}

        for section, keys in ini.dict().items():
            data[section] = {}
            for key, value in keys.items():
                data[section][key] = json.loads(value)

        return cls(data)


YAMLSerializer.represent_dict_for_class(benedict)
