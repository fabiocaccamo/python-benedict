import json

from benedict.dicts import benedict as _benedict


class benedict(_benedict):
    def to_ini(self, *args, **kwargs):
        def super_class(*vargs):
            return self.__class__.__bases__[0](*vargs)

        data = {}

        for section, keys in self.dict().items():
            data[section] = {}
            for key, value in keys.items():
                data[section][key] = json.dumps(value)

        return super_class(data).to_ini(*args, **kwargs)

    @classmethod
    def from_ini(cls, s, **kwargs):
        ini = super().from_ini(s, **kwargs)

        data = {}

        for section, keys in ini.dict().items():
            data[section] = {}
            for key, value in keys.items():
                data[section][key] = json.loads(value)

        return cls(data)
