# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

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
        if not type_util.is_string(data) and subformat:
            from benedict.serializers import get_serializer_by_format
            serializer = get_serializer_by_format(subformat)
            if serializer:
                data = serializer.encode(data, **kwargs)
        if type_util.is_string(data) and encoding:
            data = data.encode(encoding)
        data = base64.b64encode(data)
        if type_util.is_binary(data) and encoding:
            data = data.decode(encoding)
        return data
