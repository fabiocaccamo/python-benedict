# -*- coding: utf-8 -*-


class AbstractSerializer(object):

    def __init__(self):
        super(AbstractSerializer, self).__init__()

    def decode(self, s, **kwargs):
        raise NotImplementedError()

    def encode(self, d, **kwargs):
        raise NotImplementedError()
