# -*- coding: utf-8 -*-

from benedict.serializers import JSONSerializer
from benedict.utils import type_util

from six import text_type


def _encoder(obj):
    if not type_util.is_json_serializable(obj):
        return text_type(obj)


def dump(obj, **kwargs):
    serializer = JSONSerializer
    options = {
        'indent': 4,
        'sort_keys': True,
        'default': _encoder,
    }
    options.update(**kwargs)
    try:
        output = serializer.encode(obj, **options)
        return output
    except TypeError as error:
        sort_keys = options.pop('sort_keys', False)
        if sort_keys:
            output = serializer.encode(obj, **options)
            return output
        raise error
