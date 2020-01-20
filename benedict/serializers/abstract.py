# -*- coding: utf-8 -*-


class AbstractSerializer(object):

    def __init__(self):
        super(AbstractSerializer, self).__init__()

    def decode(self, s, **kwargs):
        pass

    def encode(self, d, **kwargs):
        pass
