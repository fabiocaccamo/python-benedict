# -*- coding: utf-8 -*-

import base64
import errno
import json
import os
import requests
import xmltodict
import toml
import yaml

def decode_base64(s, **kwargs):
    decode_format = kwargs.pop('format', 'json').lower()
    decoders = {
        'json': decode_json,
        'toml': decode_toml,
        'yaml': decode_yaml,
        'xml': decode_xml,
    }
    decode_func = decoders.get(decode_format, decode_json)
    b = base64.b64decode(s)
    s = b.decode('utf-8')
    return decode_func(s, **kwargs)


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
    encode_format = kwargs.pop('format', 'json').lower()
    encoders = {
        'json': encode_json,
        'toml': encode_toml,
        'yaml': encode_yaml,
        'xml': encode_xml,
    }
    encode_func = encoders.get(encode_format, encode_json)
    data = base64.b64encode(
        encode_func(d, **kwargs).encode('utf-8')).decode('utf-8')
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
