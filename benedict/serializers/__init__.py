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


_SERIALIZERS = {
    'b64': Base64Serializer,
    'base64': Base64Serializer,
    'csv': CSVSerializer,
    'json': JSONSerializer,
    'pickle': PickleSerializer,
    'qs': QueryStringSerializer,
    'querystring': QueryStringSerializer,
    'query-string': QueryStringSerializer,
    'query_string': QueryStringSerializer,
    'toml': TOMLSerializer,
    'yaml': YAMLSerializer,
    'yml': YAMLSerializer,
    'xml': XMLSerializer,
}

_SERIALIZERS_EXTENSIONS = [
    '.{}'.format(extension) for extension in _SERIALIZERS.keys()]


def get_serializer_by_format(format):
    return _SERIALIZERS.get(format.lower().replace(' ', '_'))


def get_serializers_extensions():
    return list(_SERIALIZERS_EXTENSIONS)
