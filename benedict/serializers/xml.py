try:
    import xmltodict

    xml_installed = True
except ModuleNotFoundError:
    xml_installed = False


from benedict.extras import require_xml
from benedict.serializers.abstract import AbstractSerializer


class XMLSerializer(AbstractSerializer):
    """
    This class describes a xml serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "xml",
            ],
        )

    def decode(self, s, **kwargs):
        require_xml(installed=xml_installed)
        kwargs.setdefault("dict_constructor", dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def encode(self, d, **kwargs):
        require_xml(installed=xml_installed)
        data = xmltodict.unparse(d, **kwargs)
        return data
