# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer

from six import binary_type, string_types

try:
    # python 3
    from urllib.parse import unquote
except ImportError:
    # python 2
    from urllib import unquote

import base64


class Base64Serializer(AbstractSerializer):

    def __init__(self):
        super(Base64Serializer, self).__init__()

    def decode(self, s, **kwargs):
        # fix urlencoded chars
        s = unquote(s)
        # fix padding
        m = len(s) % 4
        if m != 0:
            s += '=' * (4 - m)
        data = base64.b64decode(s)
        subformat = kwargs.pop('subformat', None)
        encoding = kwargs.pop('encoding', 'utf-8' if subformat else None)
        if encoding:
            data = data.decode(encoding)
            if subformat:
                from benedict.serializers import get_serializer_by_format
                serializer = get_serializer_by_format(subformat)
                if serializer:
                    data = serializer.decode(data, **kwargs)
        return data

    def encode(self, d, **kwargs):
        data = d
        subformat = kwargs.pop('subformat', None)
        encoding = kwargs.pop('encoding', 'utf-8' if subformat else None)
        if not isinstance(data, string_types) and subformat:
            from benedict.serializers import get_serializer_by_format
            serializer = get_serializer_by_format(subformat)
            if serializer:
                data = serializer.encode(data, **kwargs)
        if isinstance(data, string_types) and encoding:
            data = data.encode(encoding)
        data = base64.b64encode(data)
        if isinstance(data, binary_type) and encoding:
            data = data.decode(encoding)
        return data
