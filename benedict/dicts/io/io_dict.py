from __future__ import annotations

import traceback
from pathlib import Path
from typing import Any, NoReturn, cast

from typing_extensions import Self, TypeVar

from benedict.dicts.base import BaseDict
from benedict.dicts.io import io_util
from benedict.exceptions import ExtrasRequireModuleNotFoundError
from benedict.utils import type_util

_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)


class IODict(BaseDict[_K, _V]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructs a new instance.
        """
        # if first argument is data-string, url
        # or filepath (str or pathlib.Path) try to decode it.
        # use 'format' kwarg to specify the decoder to use, default 'json'.
        if len(args) == 1:
            arg = args[0]
            if type_util.is_string(arg) or type_util.is_path(arg):
                d = IODict._decode_init(arg, **kwargs)
                super().__init__(d)
                return
        super().__init__(*args, **kwargs)

    @staticmethod
    def _decode_init(s: str | Path, **kwargs: Any) -> dict[str, Any]:
        autodetected_format = io_util.autodetect_format(s)
        default_format = autodetected_format or "json"
        format = kwargs.pop("format", default_format).lower()
        # decode data-string and initialize with dict data.
        return IODict._decode(s, format, **kwargs)

    @staticmethod
    def _decode(s: str | Path, format: str, **kwargs: Any) -> dict[str, Any]:
        data = None
        try:
            data = io_util.decode(s, format, **kwargs)
        except ExtrasRequireModuleNotFoundError as e:
            raise e
        except Exception as error:
            error_traceback = traceback.format_exc()
            raise ValueError(
                f"{error_traceback}\n"
                f"Unexpected error / Invalid data or url or filepath argument: {s}\n{error}"
            ) from None
        # if possible return data as dict, otherwise raise exception
        if type_util.is_dict(data):
            return data
        elif type_util.is_list(data):
            # force list to dict
            return {"values": data}
        else:
            raise ValueError(f"Invalid data type: {type(data)}, expected dict or list.")

    @staticmethod
    def _encode(d: Any, format: str, **kwargs: Any) -> Any:
        s = io_util.encode(d, format, **kwargs)
        return s

    @classmethod
    def from_base64(
        cls, s: str, subformat: str = "json", encoding: str = "utf-8", **kwargs: Any
    ) -> Self:
        """
        Load and decode Base64 data from url, filepath or data-string.
        Data is decoded according to subformat and encoding.
        Decoder specific options can be passed using kwargs.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs["subformat"] = subformat
        kwargs["encoding"] = encoding
        return cls(s, format="base64", **kwargs)

    @classmethod
    def from_cli(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode data from a string of CLI arguments.
        ArgumentParser specific options can be passed using kwargs:
        https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="cli", **kwargs)

    @classmethod
    def from_csv(
        cls, s: str, columns: Any = None, columns_row: bool = True, **kwargs: Any
    ) -> Self:
        """
        Load and decode CSV data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/csv.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return cls(s, format="csv", **kwargs)

    @classmethod
    def from_html(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode html data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://beautiful-soup-4.readthedocs.io/
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="html", **kwargs)

    @classmethod
    def from_ini(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode INI data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="ini", **kwargs)

    @classmethod
    def from_json(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode JSON data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="json", **kwargs)

    @classmethod
    def from_pickle(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode a pickle encoded in Base64 format from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="pickle", **kwargs)

    @classmethod
    def from_plist(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode p-list data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="plist", **kwargs)

    @classmethod
    def from_query_string(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode query-string from url, filepath or data-string.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="query_string", **kwargs)

    @classmethod
    def from_toml(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode TOML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="toml", **kwargs)

    @classmethod
    def from_xls(
        cls,
        s: Path | str,
        sheet: int = 0,
        columns: Any = None,
        columns_row: bool = True,
        **kwargs: Any,
    ) -> Self:
        """
        Load and decode XLS files (".xls", ".xlsx", ".xlsm") from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        - https://openpyxl.readthedocs.io/ (for .xlsx and .xlsm files)
        - https://pypi.org/project/xlrd/ (for .xls files)
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs["sheet"] = sheet
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return cls(s, format="xls", **kwargs)

    @classmethod
    def from_xml(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode XML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="xml", **kwargs)

    @classmethod
    def from_yaml(cls, s: str, **kwargs: Any) -> Self:
        """
        Load and decode YAML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="yaml", **kwargs)

    def to_base64(
        self, subformat: str = "json", encoding: str = "utf-8", **kwargs: Any
    ) -> str:
        """
        Encode the current dict instance in Base64 format
        using the given subformat and encoding.
        Encoder specific options can be passed using kwargs.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["subformat"] = subformat
        kwargs["encoding"] = encoding
        return cast("str", self._encode(self.dict(), "base64", **kwargs))

    def to_cli(self, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    def to_csv(
        self,
        key: _K | str = "values",
        columns: Any = None,
        columns_row: bool = True,
        **kwargs: Any,
    ) -> str:
        """
        Encode a list of dicts in the current dict instance in CSV format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/csv.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return cast("str", self._encode(self.dict()[key], "csv", **kwargs))  # type: ignore[index]

    def to_html(self, **kwargs: Any) -> NoReturn:
        raise NotImplementedError

    def to_ini(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in INI format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "ini", **kwargs))

    def to_json(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in JSON format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "json", **kwargs))

    def to_pickle(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance as pickle (encoded in Base64).
        The pickle protocol used by default is 2.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "pickle", **kwargs))

    def to_plist(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance as p-list.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "plist", **kwargs))

    def to_query_string(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in query-string format.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "query_string", **kwargs))

    def to_toml(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in TOML format.
        Encoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "toml", **kwargs))

    def to_xml(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in XML format.
        Encoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "xml", **kwargs))

    def to_xls(
        self,
        key: _K | str = "values",
        sheet: int = 0,
        columns: Any = None,
        columns_row: bool = True,
        format: str = "xlsx",
        **kwargs: Any,
    ) -> NoReturn:
        """
        Encode a list of dicts in the current dict instance in XLS format.
        Encoder specific options can be passed using kwargs:
        - https://openpyxl.readthedocs.io/ (for .xlsx and .xlsm files)
        - https://pypi.org/project/xlrd/ (for .xls files)
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        # kwargs["sheet"] = sheet
        # kwargs["columns"] = columns
        # kwargs["columns_row"] = columns_row
        # kwargs["format"] = format
        # return self._encode(self.dict()[key], "xls", **kwargs)
        raise NotImplementedError

    def to_yaml(self, **kwargs: Any) -> str:
        """
        Encode the current dict instance in YAML format.
        Encoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return cast("str", self._encode(self.dict(), "yaml", **kwargs))
