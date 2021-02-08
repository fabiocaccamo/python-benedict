# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

try:
    # python 3
    from urllib.parse import urlencode
    from urllib.parse import parse_qs
except ImportError:
    # python 2
    from urllib import urlencode
    from urlparse import parse_qs

import re


class QueryStringSerializer(AbstractSerializer):

    def __init__(self):
        super(QueryStringSerializer, self).__init__()

    def decode(self, s, **kwargs):
        flat = kwargs.pop('flat', True)
        qs_re = r'(?:([\w\-\%\+\.\|]+\=[\w\-\%\+\.\|]*)+(?:[\&]{1})?)+'
        qs_pattern = re.compile(qs_re)
        if qs_pattern.match(s):
            data = parse_qs(s)
            if flat:
                data = {key: value[0] for key, value in data.items()}
            return data
        raise ValueError('Invalid query string: {}'.format(s))

    def encode(self, d, **kwargs):
        data = urlencode(d, **kwargs)
        return data
