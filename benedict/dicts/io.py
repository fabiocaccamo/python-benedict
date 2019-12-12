# -*- coding: utf-8 -*-

from benedict.utils import io_util

from six import string_types, text_type


class IODict(dict):

    def __init__(self, *args, **kwargs):
        """
        Constructs a new instance.
        """
        # if first argument is data-string try to decode it.
        # use 'format' kwarg to specify the decoder to use, default 'json'.
        if len(args) and isinstance(args[0], string_types):
            s = args[0]
            format = kwargs.pop('format', 'json').lower()
            if format in ['b64', 'base64']:
                kwargs.setdefault('subformat', 'json')
            # decode data-string and initialize with dict data.
            d = IODict._decode(s, format, **kwargs)
            if d and isinstance(d, dict):
                super(IODict, self).__init__(d)
            else:
                raise ValueError('Invalid string data input.')
        else:
            super(IODict, self).__init__(*args, **kwargs)

    @staticmethod
    def _decode(s, format, **kwargs):
        d = None
        try:
            content = io_util.read_content(s)
            # decode content using the given format
            data = io_util.decode(content, format, **kwargs)
            if isinstance(data, dict):
                d = data
            elif isinstance(data, list):
                # force list to dict
                d = { 'values': data }
            else:
                raise ValueError(
                    'Invalid data type: {}, expected dict or list.'.format(type(data)))
        except Exception as e:
            raise ValueError(
                'Invalid data or url or filepath input argument: {}\n{}'.format(s, text_type(e)))
        return d

    @staticmethod
    def _encode(d, format, **kwargs):
        filepath = kwargs.pop('filepath', None)
        s = io_util.encode(d, format, **kwargs)
        if filepath:
            io_util.write_file(filepath, s)
        return s

    @classmethod
    def from_base64(cls, s, subformat='json', encoding='utf-8', **kwargs):
        """
        Load and decode Base64 data from url, filepath or data-string.
        Data is decoded according to subformat and encoding.
        Decoder specific options can be passed using kwargs.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs['subformat'] = subformat
        kwargs['encoding'] = encoding
        return cls(IODict._decode(s, 'base64', **kwargs))

    @classmethod
    def from_csv(cls, s, columns=None, columns_row=True, **kwargs):
        """
        Load and decode CSV data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs: https://docs.python.org/3/library/csv.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        kwargs['columns'] = columns
        kwargs['columns_row'] = columns_row
        return cls(IODict._decode(s, 'csv', **kwargs))

    @classmethod
    def from_json(cls, s, **kwargs):
        """
        Load and decode JSON data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs: https://docs.python.org/3/library/json.html
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(IODict._decode(s, 'json', **kwargs))

    @classmethod
    def from_query_string(cls, s, **kwargs):
        """
        Load and decode query-string from url, filepath or data-string.
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(IODict._decode(s, 'query_string', **kwargs))

    @classmethod
    def from_toml(cls, s, **kwargs):
        """
        Load and decode TOML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs: https://pypi.org/project/toml/
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(IODict._decode(s, 'toml', **kwargs))

    @classmethod
    def from_xml(cls, s, **kwargs):
        """
        Load and decode XML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs: https://github.com/martinblech/xmltodict
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(IODict._decode(s, 'xml', **kwargs))

    @classmethod
    def from_yaml(cls, s, **kwargs):
        """
        Load and decode YAML data from url, filepath or data-string.
        Decoder specific options can be passed using kwargs: https://pyyaml.org/wiki/PyYAMLDocumentation
        Return a new dict instance. A ValueError is raised in case of failure.
        """
        return cls(IODict._decode(s, 'yaml', **kwargs))

    def to_base64(self, subformat='json', encoding='utf-8', **kwargs):
        """
        Encode the current dict instance in Base64 format using the given subformat and encoding.
        Encoder specific options can be passed using kwargs.
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs['subformat'] = subformat
        kwargs['encoding'] = encoding
        return IODict._encode(self, 'base64', **kwargs)

    def to_csv(self, key='values', columns=None, columns_row=True, **kwargs):
        """
        Encode the current dict instance in CSV format.
        Encoder specific options can be passed using kwargs: https://docs.python.org/3/library/csv.html
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        kwargs['columns'] = columns
        kwargs['columns_row'] = columns_row
        return IODict._encode(self[key], 'csv', **kwargs)

    def to_json(self, **kwargs):
        """
        Encode the current dict instance in JSON format.
        Encoder specific options can be passed using kwargs: https://docs.python.org/3/library/json.html
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        return IODict._encode(self, 'json', **kwargs)

    def to_query_string(self, **kwargs):
        """
        Encode the current dict instance in query-string format.
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        return IODict._encode(self, 'query_string', **kwargs)

    def to_toml(self, **kwargs):
        """
        Encode the current dict instance in TOML format.
        Encoder specific options can be passed using kwargs: https://pypi.org/project/toml/
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        return IODict._encode(self, 'toml', **kwargs)

    def to_xml(self, **kwargs):
        """
        Encode the current dict instance in XML format.
        Encoder specific options can be passed using kwargs: https://github.com/martinblech/xmltodict
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        return IODict._encode(self, 'xml', **kwargs)

    def to_yaml(self, **kwargs):
        """
        Encode the current dict instance in YAML format.
        Encoder specific options can be passed using kwargs: https://pyyaml.org/wiki/PyYAMLDocumentation
        Return the encoded string and optionally save it at the specified 'filepath'.
        A ValueError is raised in case of failure.
        """
        return IODict._encode(self, 'yaml', **kwargs)
