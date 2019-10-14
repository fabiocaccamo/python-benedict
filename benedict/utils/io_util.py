# -*- coding: utf-8 -*-

from six import string_types

import base64
import errno
import json
import os
import requests
import xmltodict
import toml
import yaml

try:
    # python 3
    from urllib.parse import unquote_plus as urldecode
except ImportError:
    # python 2
    from urllib import unquote_plus as urldecode


def decode_base64(s, **kwargs):
    # fix urlencoded chars
    s = urldecode(s)
    # fix padding
    m = len(s) % 4
    if m != 0:
        s += '=' * (4 - m)
    encoding = kwargs.pop('encoding', 'utf-8')
    data = base64.b64decode(s).decode(encoding)
    # decode data if format is specified
    decode_format = kwargs.pop('format', 'json')
    if decode_format:
        decoders = {
            'json': decode_json,
            'toml': decode_toml,
            'yaml': decode_yaml,
            'xml': decode_xml,
        }
        decode_func = decoders.get(decode_format.lower(), None)
        if decode_func:
            data = decode_func(data, **kwargs)
    return data


def decode_json(s, **kwargs):
    data = json.loads(s, **kwargs)
    return data


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
    encoding = kwargs.pop('encoding', 'utf-8')
    encode_format = kwargs.pop('format', 'json')
    if encode_format:
        encoders = {
            'json': encode_json,
            'toml': encode_toml,
            'yaml': encode_yaml,
            'xml': encode_xml,
        }
        encode_func = encoders.get(encode_format.lower(), None)
        if encode_func:
            data = encode_func(d, **kwargs)
    if isinstance(data, string_types):
        data = data.encode(encoding)
    data = base64.b64encode(data).decode(encoding)
    return data


def encode_json(d, **kwargs):
    data = json.dumps(d, **kwargs)
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
    content = response.text
    return content


def write_file(filepath, content):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as e:
            # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
