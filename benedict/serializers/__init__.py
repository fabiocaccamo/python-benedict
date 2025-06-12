from __future__ import annotations

import re
from typing import Any, Literal, TypedDict, cast

from typing_extensions import overload

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.base64 import Base64Serializer
from benedict.serializers.cli import CLISerializer
from benedict.serializers.csv import CSVSerializer
from benedict.serializers.html import HTMLSerializer
from benedict.serializers.ini import INISerializer
from benedict.serializers.json import JSONSerializer
from benedict.serializers.pickle import PickleSerializer
from benedict.serializers.plist import PListSerializer
from benedict.serializers.query_string import QueryStringSerializer
from benedict.serializers.toml import TOMLSerializer
from benedict.serializers.xls import XLSSerializer
from benedict.serializers.xml import XMLSerializer
from benedict.serializers.yaml import YAMLSerializer

__all__ = [
    "AbstractSerializer",
    "Base64Serializer",
    "CLISerializer",
    "CSVSerializer",
    "HTMLSerializer",
    "INISerializer",
    "JSONSerializer",
    "PickleSerializer",
    "PListSerializer",
    "QueryStringSerializer",
    "TOMLSerializer",
    "XLSSerializer",
    "XMLSerializer",
    "YAMLSerializer",
]

_BASE64_SERIALIZER = Base64Serializer()
_CLI_SERIALIZER = CLISerializer()
_CSV_SERIALIZER = CSVSerializer()
_HTML_SERIALIZER = HTMLSerializer()
_INI_SERIALIZER = INISerializer()
_JSON_SERIALIZER = JSONSerializer()
_PICKLE_SERIALIZER = PickleSerializer()
_PLIST_SERIALIZER = PListSerializer()
_QUERY_STRING_SERIALIZER = QueryStringSerializer()
_TOML_SERIALIZER = TOMLSerializer()
_XLS_SERIALIZER = XLSSerializer()
_XML_SERIALIZER = XMLSerializer()
_YAML_SERIALIZER = YAMLSerializer()

_SERIALIZERS_LIST: list[AbstractSerializer[Any, Any]] = [
    _BASE64_SERIALIZER,
    _CLI_SERIALIZER,
    _CSV_SERIALIZER,
    _HTML_SERIALIZER,
    _INI_SERIALIZER,
    _JSON_SERIALIZER,
    _PICKLE_SERIALIZER,
    _PLIST_SERIALIZER,
    _QUERY_STRING_SERIALIZER,
    _TOML_SERIALIZER,
    _YAML_SERIALIZER,
    _XLS_SERIALIZER,
    _XML_SERIALIZER,
]


class SerializersByExtension(TypedDict, total=False):
    b64: Base64Serializer
    base64: Base64Serializer
    cli: CLISerializer
    csv: CSVSerializer
    html: HTMLSerializer
    ini: INISerializer
    json: JSONSerializer
    pickle: PickleSerializer
    plist: PListSerializer
    qs: QueryStringSerializer
    querystring: QueryStringSerializer
    toml: TOMLSerializer
    xls: XLSSerializer
    xlsx: XLSSerializer
    xlsm: XLSSerializer
    xml: XMLSerializer
    yaml: YAMLSerializer


_SERIALIZERS_BY_EXTENSION: SerializersByExtension = {}
FormatExtension = Literal[
    "base64",
    "b64",
    "cli",
    "csv",
    "html",
    "json",
    "pickle",
    "plist",
    "qs",
    "querystring",
    "toml",
    "xls",
    "xlsx",
    "xlsm",
    "xml",
]
for serializer in _SERIALIZERS_LIST:
    for extension in serializer.extensions():
        _SERIALIZERS_BY_EXTENSION[extension] = serializer  # type: ignore[literal-required]

_SERIALIZERS_EXTENSIONS = [
    f".{extension}" for extension in _SERIALIZERS_BY_EXTENSION.keys()
]


def get_format_by_path(path: Any) -> str | None:
    path = str(path)
    path = path.lower()
    for extension in _SERIALIZERS_EXTENSIONS:
        if path.endswith(extension):
            return extension[1:]
    return None


@overload
def get_serializer_by_format(format: Literal["base64", "b64"]) -> Base64Serializer: ...


@overload
def get_serializer_by_format(format: Literal["cli"]) -> CLISerializer: ...


@overload
def get_serializer_by_format(format: Literal["csv"]) -> CSVSerializer: ...


@overload
def get_serializer_by_format(format: Literal["html"]) -> HTMLSerializer: ...


@overload
def get_serializer_by_format(format: Literal["json"]) -> JSONSerializer: ...


@overload
def get_serializer_by_format(format: Literal["pickle"]) -> PickleSerializer: ...


@overload
def get_serializer_by_format(
    format: Literal["qs", "querystring"],
) -> QueryStringSerializer: ...


@overload
def get_serializer_by_format(format: Literal["toml"]) -> TOMLSerializer: ...


@overload
def get_serializer_by_format(
    format: Literal["xls", "xlsx", "xlsm"],
) -> XLSSerializer: ...


@overload
def get_serializer_by_format(format: Literal["xml"]) -> XMLSerializer: ...


@overload
def get_serializer_by_format(format: str) -> AbstractSerializer[Any, Any]: ...


def get_serializer_by_format(
    format: FormatExtension | str,
) -> (
    Base64Serializer
    | CLISerializer
    | CSVSerializer
    | HTMLSerializer
    | JSONSerializer
    | PickleSerializer
    | PListSerializer
    | QueryStringSerializer
    | TOMLSerializer
    | XLSSerializer
    | XMLSerializer
    | AbstractSerializer[Any, Any]
):
    format_key = cast("FormatExtension", format.lower().strip())
    format_key = cast("FormatExtension", re.sub(r"[\s\-\_]*", "", format_key))
    serializer = _SERIALIZERS_BY_EXTENSION[format_key]
    return serializer
