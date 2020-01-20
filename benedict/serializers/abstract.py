# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class AbstractSerializer(ABC):

    def __init__(self):
        super(AbstractSerializer, self).__init__()

    @abstractmethod
    def decode(self, s, **kwargs):
        pass

    @abstractmethod
    def encode(self, d, **kwargs):
        pass
