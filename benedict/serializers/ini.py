# -*- coding: utf-8 -*-

from benedict.serializers.abstract import AbstractSerializer
from benedict.utils import type_util

from configparser import ConfigParser
from configparser import DEFAULTSECT as default_section
from io import StringIO


class INISerializer(AbstractSerializer):
    """
    This class describes an ini serializer.
    """

    def __init__(self):
        super(INISerializer, self).__init__(
            extensions=[
                "ini",
            ],
        )

    @staticmethod
    def _get_section_option_value(parser, section, option):
        value = None
        funcs = [parser.getint, parser.getfloat, parser.getboolean, parser.get]
        for func in funcs:
            try:
                value = func(section, option)
                break
            except ValueError:
                continue
        return value

    def decode(self, s, **kwargs):
        parser = ConfigParser(**kwargs)
        parser.read_string(s)
        data = {}
        for option, _ in parser.defaults().items():
            data[option] = self._get_section_option_value(
                parser, default_section, option
            )
        for section in parser.sections():
            data[section] = {}
            for option, _ in parser.items(section):
                data[section][option] = self._get_section_option_value(
                    parser, section, option
                )
        return data

    def encode(self, d, **kwargs):
        parser = ConfigParser(**kwargs)
        for key, value in d.items():
            if not type_util.is_dict(value):
                parser.set(default_section, key, f"{value}")
                continue
            section = key
            parser.add_section(section)
            for option_key, option_value in value.items():
                parser.set(section, option_key, f"{option_value}")
        str_data = StringIO()
        parser.write(str_data)
        return str_data.getvalue()
