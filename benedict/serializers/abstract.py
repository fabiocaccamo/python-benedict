# -*- coding: utf-8 -*-


class AbstractSerializer(object):
    """
    This class describes an abstract serializer.
    """

    def __init__(self):
        super(AbstractSerializer, self).__init__()

    def decode(self, s, **kwargs):
        raise NotImplementedError()

    def encode(self, d, **kwargs):
        raise NotImplementedError()
