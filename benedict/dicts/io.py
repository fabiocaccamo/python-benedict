# -*- coding: utf-8 -*-

from benedict.utils import io_util

from six import string_types, text_type


class IODict(dict):

    def __init__(self, *args, **kwargs):
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

    @staticmethod
    def from_base64(s, subformat='json', encoding='utf-8', **kwargs):
        kwargs['subformat'] = subformat
        kwargs['encoding'] = encoding
        return IODict._decode(s, 'base64', **kwargs)

    @staticmethod
    def from_csv(s, columns=None, columns_row=True, **kwargs):
        kwargs['columns'] = columns
        kwargs['columns_row'] = columns_row
        return IODict._decode(s, 'csv', **kwargs)

    @staticmethod
    def from_json(s, **kwargs):
        return IODict._decode(s, 'json', **kwargs)

    @staticmethod
    def from_query_string(s, **kwargs):
        return IODict._decode(s, 'query_string', **kwargs)

    @staticmethod
    def from_toml(s, **kwargs):
        return IODict._decode(s, 'toml', **kwargs)

    @staticmethod
    def from_xml(s, **kwargs):
        return IODict._decode(s, 'xml', **kwargs)

    @staticmethod
    def from_yaml(s, **kwargs):
        return IODict._decode(s, 'yaml', **kwargs)

    def to_base64(self, subformat='json', encoding='utf-8', **kwargs):
        kwargs['subformat'] = subformat
        kwargs['encoding'] = encoding
        return IODict._encode(self, 'base64', **kwargs)

    def to_csv(self, key='values', columns=None, columns_row=True, **kwargs):
        kwargs['columns'] = columns
        kwargs['columns_row'] = columns_row
        return IODict._encode(self[key], 'csv', **kwargs)

    def to_json(self, **kwargs):
        return IODict._encode(self, 'json', **kwargs)

    def to_query_string(self, **kwargs):
        return IODict._encode(self, 'query_string', **kwargs)

    def to_toml(self, **kwargs):
        return IODict._encode(self, 'toml', **kwargs)

    def to_xml(self, **kwargs):
        return IODict._encode(self, 'xml', **kwargs)

    def to_yaml(self, **kwargs):
        return IODict._encode(self, 'yaml', **kwargs)
