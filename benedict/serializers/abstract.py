# -*- coding: utf-8 -*-


class AbstractSerializer(object):
    """
    This class describes an abstract serializer.
    """

    def __init__(self, extensions=None):
        super(AbstractSerializer, self).__init__()
        self._extensions = (extensions or []).copy()

    def decode(self, s, **kwargs):
        raise NotImplementedError()

    def encode(self, d, **kwargs):
        raise NotImplementedError()

    def extensions(self):
        return self._extensions.copy()
