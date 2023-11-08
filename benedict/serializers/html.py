try:
    from bs4 import BeautifulSoup

    html_installed = True
except ModuleNotFoundError:
    html_installed = False

from benedict.extras import require_html
from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.xml import XMLSerializer


class HTMLSerializer(AbstractSerializer):
    """
    This class describes a html serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "html",
            ],
        )

    def decode(self, s, **kwargs):
        require_html(installed=html_installed)
        html_content = s
        soup = BeautifulSoup(html_content, "html.parser")
        xml_content = soup.prettify()
        xml_serializer = XMLSerializer()
        data = xml_serializer.decode(xml_content)
        return data

    def encode(self, d, **kwargs):
        raise NotImplementedError
