from __future__ import annotations

try:
    import xmltodict

    xml_installed = True
except ModuleNotFoundError:
    xml_installed = False


from typing import Any, cast

from benedict.extras import require_xml
from benedict.serializers.abstract import AbstractSerializer


class XMLSerializer(AbstractSerializer[str, dict[str, Any]]):
    """
    This class describes a xml serializer.
    """

    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "xml",
            ],
        )

    def decode(self, s: str, **kwargs: Any) -> dict[str, Any]:
        require_xml(installed=xml_installed)
        kwargs.setdefault("dict_constructor", dict)
        data = xmltodict.parse(s, **kwargs)
        return data

    def encode(self, d: dict[str, Any], **kwargs: Any) -> str:
        require_xml(installed=xml_installed)
        data = xmltodict.unparse(d, **kwargs)
        return cast("str", data)
