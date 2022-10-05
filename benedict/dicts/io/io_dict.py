# -*- coding: utf-8 -*-

from benedict.dicts.base import BaseDict
from benedict.dicts.io import io_util
from benedict.utils import type_util


class IODict(BaseDict):
    def __init__(self, *args, **kwargs):
        """
        Constructs a new instance.
        """
        # if first argument is data-string, url or filepath try to decode it.
        # use 'format' kwarg to specify the decoder to use, default 'json'.
        if len(args) == 1 and type_util.is_string(args[0]):
            d = IODict._decode_init(args[0], **kwargs)
            super(IODict, self).__init__(d)
            return
        super(IODict, self).__init__(*args, **kwargs)

    @staticmethod
    def _decode_init(s, **kwargs):
        autodetected_format = io_util.autodetect_format(s)
        default_format = autodetected_format or "json"
        format = kwargs.pop("format", default_format).lower()
        # decode data-string and initialize with dict data.
        return IODict._decode(s, format, **kwargs)

    @staticmethod
    def _decode(s, format, **kwargs):
        data = None
        try:
            data = io_util.decode(s, format, **kwargs)
        except Exception as e:
            raise ValueError(f"Invalid data or url or filepath argument: {s}\n{e}")
        # if possible return data as dict, otherwise raise exception
        if type_util.is_dict(data):
            return data
        elif type_util.is_list(data):
            # force list to dict
            return {"values": data}
        else:
            raise ValueError(f"Invalid data type: {type(data)}, expected dict or list.")

    @staticmethod
    def _encode(d, format, **kwargs):
        filepath = kwargs.pop("filepath", None)
        s = io_util.encode(d, format, **kwargs)
        if filepath:
            io_util.write_file(filepath, s)
        return s

    @classmethod
    def from_base64(cls, s, subformat="json", encoding="utf-8", **kwargs):
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
    def from_csv(cls, s, columns=None, columns_row=True, **kwargs):
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
    def from_ini(cls, s, **kwargs):
        """
        Load and decode INI data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="ini", **kwargs)

    @classmethod
    def from_json(cls, s, **kwargs):
        """
        Load and decode JSON data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="json", **kwargs)

    @classmethod
    def from_pickle(cls, s, **kwargs):
        """
        Load and decode a pickle encoded in Base64 format data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="pickle", **kwargs)

    @classmethod
    def from_plist(cls, s, **kwargs):
        """
        Load and decode p-list data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="plist", **kwargs)

    @classmethod
    def from_query_string(cls, s, **kwargs):
        """
        Load and decode query-string from url, filepath or data-string.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="query_string", **kwargs)

    @classmethod
    def from_toml(cls, s, **kwargs):
        """
        Load and decode TOML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="toml", **kwargs)

    @classmethod
    def from_xls(cls, s, sheet=0, columns=None, columns_row=True, **kwargs):
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
    def from_xml(cls, s, **kwargs):
        """
        Load and decode XML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="xml", **kwargs)

    @classmethod
    def from_yaml(cls, s, **kwargs):
        """
        Load and decode YAML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(s, format="yaml", **kwargs)

    def to_base64(self, subformat="json", encoding="utf-8", **kwargs):
        """
        Encode the current dict instance in Base64 format
        using the given subformat and encoding.
        Encoder specific options can be passed using kwargs.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["subformat"] = subformat
        kwargs["encoding"] = encoding
        return self._encode(self.dict(), "base64", **kwargs)

    def to_csv(self, key="values", columns=None, columns_row=True, **kwargs):
        """
        Encode a list of dicts in the current dict instance in CSV format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/csv.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs["columns"] = columns
        kwargs["columns_row"] = columns_row
        return self._encode(self.dict()[key], "csv", **kwargs)

    def to_ini(self, **kwargs):
        """
        Encode the current dict instance in INI format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/configparser.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "ini", **kwargs)

    def to_json(self, **kwargs):
        """
        Encode the current dict instance in JSON format.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/json.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "json", **kwargs)

    def to_pickle(self, **kwargs):
        """
        Encode the current dict instance as pickle (encoded in Base64).
        The pickle protocol used by default is 2.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/pickle.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "pickle", **kwargs)

    def to_plist(self, **kwargs):
        """
        Encode the current dict instance as p-list.
        Encoder specific options can be passed using kwargs:
        https://docs.python.org/3/library/plistlib.html
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "plist", **kwargs)

    def to_query_string(self, **kwargs):
        """
        Encode the current dict instance in query-string format.
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "query_string", **kwargs)

    def to_toml(self, **kwargs):
        """
        Encode the current dict instance in TOML format.
        Encoder specific options can be passed using kwargs:
        https://pypi.org/project/toml/
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "toml", **kwargs)

    def to_xml(self, **kwargs):
        """
        Encode the current dict instance in XML format.
        Encoder specific options can be passed using kwargs:
        https://github.com/martinblech/xmltodict
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "xml", **kwargs)

    def to_xls(
        self,
        key="values",
        sheet=0,
        columns=None,
        columns_row=True,
        format="xlsx",
        **kwargs,
    ):
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

    def to_yaml(self, **kwargs):
        """
        Encode the current dict instance in YAML format.
        Encoder specific options can be passed using kwargs:
        https://pyyaml.org/wiki/PyYAMLDocumentation
        Return the encoded string and optionally save it at 'filepath'.
        A ValueError is raised in case of failure.
        """
        return self._encode(self.dict(), "yaml", **kwargs)
