# -*- coding: utf-8 -*-

from six import binary_type, string_types

import base64
import errno
import json
import os
import re
import requests
import xmltodict
import toml
import yaml

try:
    # python 3
    from urllib.parse import unquote
    from urllib.parse import unquote_plus
    from urllib.parse import urlencode
    from urllib.parse import parse_qs
except ImportError:
    # python 2
    from urllib import unquote
    from urllib import unquote_plus
    from urllib import urlencode
    from urlparse import parse_qs


def decode_base64(s, **kwargs):
    # fix urlencoded chars
    s = unquote(s)
    # fix padding
    m = len(s) % 4
    if m != 0:
        s += '=' * (4 - m)
    data = base64.b64decode(s)
    format = kwargs.pop('format', None)
    encoding = kwargs.pop('encoding', 'utf-8' if format else None)
    if encoding:
        data = data.decode(encoding)
        if format:
            decoders = {
                'json': decode_json,
                'toml': decode_toml,
                'yaml': decode_yaml,
                'xml': decode_xml,
            }
            decode_func = decoders.get(format.lower(), '')
            if decode_func:
                data = decode_func(data, **kwargs)
    return data


def decode_json(s, **kwargs):
    data = json.loads(s, **kwargs)
    return data


def decode_query_string(s, **kwargs):
    flat = kwargs.pop('flat', True)
    qs_re = r'^(([\w\-\%\+]+\=[\w\-\%\+]*)+([\&]{1})?)+'
    qs_pattern = re.compile(qs_re)
    if qs_pattern.match(s):
        data = parse_qs(s)
        if flat:
            data = { key:value[0] for key, value in data.items() }
        return data
    else:
        raise ValueError('Invalid query string: {}'.format(s))


def decode_xml(s, **kwargs):
    kwargs.setdefault('dict_constructor', dict)
    data = xmltodict.parse(s, **kwargs)
    return data


def decode_toml(s, **kwargs):
    data = toml.loads(s, **kwargs)
    return data


def decode_yaml(s, **kwargs):
    kwargs.setdefault('Loader', yaml.Loader)
    data = yaml.load(s, **kwargs)
    return data


def encode_base64(d, **kwargs):
    data = d
    format = kwargs.pop('format', None)
    encoding = kwargs.pop('encoding', 'utf-8' if format else None)
    if not isinstance(data, string_types) and format:
        encoders = {
            'json': encode_json,
            'toml': encode_toml,
            'yaml': encode_yaml,
            'xml': encode_xml,
        }
        encode_func = encoders.get(format.lower(), '')
        if encode_func:
            data = encode_func(data, **kwargs)
    if isinstance(data, string_types) and encoding:
        data = data.encode(encoding)
    data = base64.b64encode(data)
    if isinstance(data, binary_type) and encoding:
        data = data.decode(encoding)
    return data


def encode_json(d, **kwargs):
    data = json.dumps(d, **kwargs)
    return data


def encode_query_string(d, **kwargs):
    data = urlencode(d, **kwargs)
    return data


def encode_toml(d, **kwargs):
    data = toml.dumps(d, **kwargs)
    return data


def encode_xml(d, **kwargs):
    data = xmltodict.unparse(d, **kwargs)
    return data


def encode_yaml(d, **kwargs):
    data = yaml.dump(d, **kwargs)
    return data


def read_content(s):
    # s -> filepath or url or data
    if s.startswith('http://') or s.startswith('https://'):
        content = read_url(s)
    elif os.path.isfile(s):
        content = read_file(s)
    else:
        content = s
    return content


def read_file(filepath):
    handler = open(filepath, 'r')
    content = handler.read()
    handler.close()
    return content


def read_url(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    if response.status_code == requests.codes.ok:
        content = response.text
        return content
    else:
        raise ValueError(
            'Invalid url response status code: {}.'.format(
                response.status_code))


def write_file(filepath, content):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    filedir = os.path.dirname(filepath)
    if not os.path.exists(filedir):
        try:
            os.makedirs(filedir)
        except OSError as e:
            # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
