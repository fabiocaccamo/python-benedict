# -*- coding: utf-8 -*-

from __future__ import absolute_import

import io
from typing import Dict

from benedict.serializers.abstract import AbstractSerializer

import configparser


class INISerializer(AbstractSerializer):

    def __init__(self):
        super(INISerializer, self).__init__()

    def decode(self, s, **kwargs):
        parser = configparser.ConfigParser()
        kwargs.setdefault("source", "<string>")
        parser.read_string(s, **kwargs)
        data = {s: dict(parser.items(s)) for s in parser.sections()}
        return data

    def encode(self, d, **kwargs):
        parser = configparser.ConfigParser()
        parser.read_dict(self._preprocessed_dict(d, **kwargs))
        with io.StringIO() as data:
            parser.write(data, **kwargs)
            data.seek(0)
            return data.getvalue()

    def _preprocessed_dict(self, d, default_namespace="default"):
        sections = {
            default_namespace: {}
        }
        for key, value in d.items():
            if isinstance(value, dict):
                sections[key] = value
            else:
                sections[default_namespace][key] = value

        for section in sections.values():
            for key, val in section.items():
                if isinstance(val, object):
                    section[key] = str(val)

        return sections
