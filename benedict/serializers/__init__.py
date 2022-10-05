# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.base64 import Base64Serializer
from benedict.serializers.csv import CSVSerializer
from benedict.serializers.ini import INISerializer
from benedict.serializers.json import JSONSerializer
from benedict.serializers.pickle import PickleSerializer
from benedict.serializers.plist import PListSerializer
from benedict.serializers.query_string import QueryStringSerializer
from benedict.serializers.toml import TOMLSerializer
from benedict.serializers.xls import XLSSerializer
from benedict.serializers.xml import XMLSerializer
from benedict.serializers.yaml import YAMLSerializer

import re


__all__ = [
    "AbstractSerializer",
    "Base64Serializer",
    "CSVSerializer",
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
_CSV_SERIALIZER = CSVSerializer()
_INI_SERIALIZER = INISerializer()
_JSON_SERIALIZER = JSONSerializer()
_PICKLE_SERIALIZER = PickleSerializer()
_PLIST_SERIALIZER = PListSerializer()
_QUERY_STRING_SERIALIZER = QueryStringSerializer()
_TOML_SERIALIZER = TOMLSerializer()
_XLS_SERIALIZER = XLSSerializer()
_XML_SERIALIZER = XMLSerializer()
_YAML_SERIALIZER = YAMLSerializer()

_SERIALIZERS_LIST = [
    _BASE64_SERIALIZER,
    _CSV_SERIALIZER,
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

_SERIALIZERS_BY_EXTENSION = {}
for serializer in _SERIALIZERS_LIST:
    for extension in serializer.extensions():
        _SERIALIZERS_BY_EXTENSION[extension] = serializer

_SERIALIZERS_EXTENSIONS = [
    f".{extension}" for extension in _SERIALIZERS_BY_EXTENSION.keys()
]


def get_format_by_path(path):
    path = path.lower()
    for extension in _SERIALIZERS_EXTENSIONS:
        if path.endswith(extension):
            return extension[1:]
    return None


def get_serializer_by_format(format):
    format_key = (format or "").lower().strip()
    format_key = re.sub(r"[\s\-\_]*", "", format_key)
    serializer = _SERIALIZERS_BY_EXTENSION.get(format_key, None)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    return serializer


def get_serializers_extensions():
    return list(_SERIALIZERS_EXTENSIONS)
