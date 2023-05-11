from benedict.dicts import benedict as _benedict
import json

class benedict(_benedict):
    def to_ini(self, *args, **kwargs):
        def super_class(*vargs):
            return self.__class__.__bases__[0](*vargs)

        data = dict()

        for section, keys in self.dict().items():
            data[section] = dict()
            for key, value in keys.items():
                data[section][key] = json.dumps(value)

        return super_class(data).to_ini(*args, **kwargs)

    @classmethod
    def from_ini(cls, s, **kwargs):
        ini = super().from_ini(s, **kwargs)

        data = dict()

        for section, keys in ini.dict().items():
            data[section] = dict()
            for key, value in keys.items():
                data[section][key] = json.loads(value)

        return cls(data)
