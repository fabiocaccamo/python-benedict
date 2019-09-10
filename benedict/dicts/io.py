# -*- coding: utf-8 -*-

from benedict.utils import io_util

from six import string_types, text_type

import os


class IODict(dict):

    def __init__(self, *args, **kwargs):
        # if first argument is string,
        # try to decode it using all decoders.
        if len(args) and isinstance(args[0], string_types):
            d = IODict._from_string(args[0])
            if d and isinstance(d, dict):
                args = list(args)
                args[0] = d
                args = tuple(args)
            else:
                raise ValueError('Invalid string data input.')
        super(IODict, self).__init__(*args, **kwargs)

    @staticmethod
    def _load_and_decode(s, decoder, **kwargs):
        d = None
        try:
            if s.startswith('http://') or s.startswith('https://'):
                content = io_util.read_url(s)
            elif os.path.isfile(s):
                content = io_util.read_file(s)
            else:
                content = s
            d = decoder(content, **kwargs)
        except Exception as e:
            raise ValueError(
                'Invalid data or url or filepath input argument: {}\n{}'.format(s, text_type(e)))
        return d

    @staticmethod
    def _encode_and_save(d, encoder, filepath=None, **kwargs):
        s = encoder(d, **kwargs)
        if filepath:
            io_util.write_file(filepath, s)
        return s

    @staticmethod
    def _from_string(s, **kwargs):
        d = None
        try:
            d = IODict.from_json(s, **kwargs)
        except ValueError:
            d = None
        return d

    @staticmethod
    def from_json(s, **kwargs):
        return IODict._load_and_decode(s,
            io_util.decode_json, **kwargs)

    def to_json(self, filepath=None, **kwargs):
        return IODict._encode_and_save(self,
            encoder=io_util.encode_json,
            filepath=filepath, **kwargs)
