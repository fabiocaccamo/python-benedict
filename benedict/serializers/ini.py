# -*- coding: utf-8 -*-

from __future__ import absolute_import

import io
from copy import deepcopy

from benedict.serializers.abstract import AbstractSerializer

import configparser


class INISerializer(AbstractSerializer):

    def __init__(self):
        super(INISerializer, self).__init__()

    @staticmethod
    def _try_parse(parser: configparser.ConfigParser, section, key):
        try:
            return parser.getint(section, key)
        except ValueError:
            try:
                return parser.getfloat(section, key)
            except ValueError:
                try:
                    return parser.getboolean(section, key)
                except ValueError:
                    return parser.get(section, key)

    def decode(self, s, **kwargs):
        parser = configparser.ConfigParser()
        kwargs.setdefault("source", "<string>")
        parser.read_string(s, **kwargs)
        data = {}
        for s in parser.sections():
            data[s] = {}
            for key, _ in parser.items(s):
                data[s][key] = INISerializer._try_parse(parser, s, key)

        return data

    def encode(self, d, **kwargs):
        parser = configparser.ConfigParser()
        processed_dict = self._preprocessed_dict(d, **kwargs)
        parser.read_dict(processed_dict)
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
                sections[key] = deepcopy(value)
            else:
                sections[default_namespace][key] = value

        # Stringify all the value
        for section in sections.values():
            for key, val in section.items():
                section[key] = str(val)

        # if the default section is empty, delete it
        if len(sections[default_namespace]) == 0:
            del sections[default_namespace]

        return sections
