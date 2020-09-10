# -*- coding: utf-8 -*-

from __future__ import absolute_import

from benedict.serializers.abstract import AbstractSerializer

import plistlib
import six
import unicodedata


class PListSerializer(AbstractSerializer):
    """
    https://docs.python.org/3/library/plistlib.html
    """
    def __init__(self):
        super(PListSerializer, self).__init__()

    def decode(self, s, **kwargs):
        if six.PY2:
            if isinstance(s, unicode):
                s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
            return plistlib.readPlistFromString(s)
        kwargs.setdefault('fmt', plistlib.FMT_XML)
        encoding = kwargs.pop('encoding', 'utf-8')
        return plistlib.loads(s.encode(encoding), **kwargs)

    def encode(self, d, **kwargs):
        if six.PY2:
            return plistlib.writePlistToString(d)
        encoding = kwargs.pop('encoding', 'utf-8')
        return plistlib.dumps(d, **kwargs).decode(encoding)
