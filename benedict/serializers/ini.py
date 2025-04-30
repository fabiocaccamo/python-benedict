from collections.abc import Callable
from configparser import DEFAULTSECT as default_section
from configparser import RawConfigParser
from io import StringIO
from json.decoder import JSONDecodeError
from typing import Any

from benedict.serializers.abstract import AbstractSerializer
from benedict.serializers.json import JSONSerializer
from benedict.utils import type_util


class INISerializer(AbstractSerializer[str, dict[str, Any]]):
    """
    This class describes an ini serializer.
    """

    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "ini",
            ],
        )
        self._json = JSONSerializer()

    @staticmethod
    def _get_parser(options: dict[str, Any]) -> RawConfigParser:
        optionxform = options.pop("optionxform", lambda key: key)
        parser = RawConfigParser(**options)
        if optionxform and callable(optionxform):
            parser.optionxform = optionxform  # type: ignore[method-assign]
        return parser

    @staticmethod
    def _get_section_option_value(
        parser: RawConfigParser, section: str, option: str
    ) -> str | int | float | bool | None:
        value = None
        funcs: list[Callable[[str, str], Any]] = [
            parser.getint,
            parser.getfloat,
            parser.getboolean,
            parser.get,
        ]
        for func in funcs:
            try:
                value = func(section, option)
                break
            except ValueError:
                continue
        return value

    def decode(self, s: str, **kwargs: Any) -> dict[str, Any]:
        parser = self._get_parser(options=kwargs)
        parser.read_string(s)
        data: dict[str, Any] = {}
        for option, _ in parser.defaults().items():
            data[option] = self._get_section_option_value(
                parser, default_section, option
            )
        for section in parser.sections():
            data[section] = {}
            for option, _ in parser.items(section):
                value = self._get_section_option_value(parser, section, option)
                if type_util.is_string(value):
                    try:
                        value_decoded = self._json.decode(value)
                        value = value_decoded
                    except JSONDecodeError:
                        pass
                data[section][option] = value
        return data

    def encode(self, d: dict[str, Any], **kwargs: Any) -> str:
        parser = self._get_parser(options=kwargs)
        for key, value in d.items():
            if not type_util.is_dict(value):
                parser.set(default_section, key, f"{value}")
                continue
            section = key
            parser.add_section(section)
            for option_key, option_value in value.items():
                if type_util.is_dict(option_value):
                    parser.set(section, option_key, self._json.encode(option_value))
                else:
                    parser.set(section, option_key, option_value)
        str_data = StringIO()
        parser.write(str_data)
        return str_data.getvalue()
