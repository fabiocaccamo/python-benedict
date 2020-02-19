# -*- coding: utf-8 -*-


class AbstractSerializer(object):

    def __init__(self):
        super(AbstractSerializer, self).__init__()

    @staticmethod
    def decode(s, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def encode(d, **kwargs):
        raise NotImplementedError()
