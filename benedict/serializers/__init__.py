# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.base64 import Base64Serializer
from benedict.serializers.csv import CSVSerializer
from benedict.serializers.json import JSONSerializer
from benedict.serializers.pickle import PickleSerializer
from benedict.serializers.query_string import QueryStringSerializer
from benedict.serializers.toml import TOMLSerializer
from benedict.serializers.xml import XMLSerializer
from benedict.serializers.yaml import YAMLSerializer

_BASE64_SERIALIZER = Base64Serializer()
_CSV_SERIALIZER = CSVSerializer()
_JSON_SERIALIZER = JSONSerializer()
_PICKLE_SERIALIZER = PickleSerializer()
_QUERY_STRING_SERIALIZER = QueryStringSerializer()
_TOML_SERIALIZER = TOMLSerializer()
_YAML_SERIALIZER = YAMLSerializer()
_XML_SERIALIZER = XMLSerializer()

_SERIALIZERS = {
    'b64': _BASE64_SERIALIZER,
    'base64': _BASE64_SERIALIZER,
    'csv': _CSV_SERIALIZER,
    'json': _JSON_SERIALIZER,
    'pickle': _PICKLE_SERIALIZER,
    'qs': _QUERY_STRING_SERIALIZER,
    'querystring': _QUERY_STRING_SERIALIZER,
    'query-string': _QUERY_STRING_SERIALIZER,
    'query_string': _QUERY_STRING_SERIALIZER,
    'toml': _TOML_SERIALIZER,
    'yaml': _YAML_SERIALIZER,
    'yml': _YAML_SERIALIZER,
    'xml': _XML_SERIALIZER,
}

_SERIALIZERS_EXTENSIONS = [
    '.{}'.format(extension) for extension in _SERIALIZERS.keys()]


def get_format_by_path(path):
    path = path.lower()
    for extension in _SERIALIZERS_EXTENSIONS:
        if path.endswith(extension):
            return extension[1:]
    return None


def get_serializer_by_format(format):
    return _SERIALIZERS.get((format or '').lower().replace(' ', '_'))


def get_serializers_extensions():
    return list(_SERIALIZERS_EXTENSIONS)
