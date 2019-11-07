# -*- coding: utf-8 -*-

from six import binary_type, string_types, StringIO
from slugify import slugify

import base64
import csv
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


def decode(s, format, **kwargs):
    decode_func = _get_format_decoder(format)
    if decode_func:
        decode_opts = kwargs.copy()
        data = decode_func(s.strip(), **decode_opts)
        return data
    else:
        raise ValueError('Invalid format: {}.'.format(format))


def decode_base64(s, **kwargs):
    # fix urlencoded chars
    s = unquote(s)
    # fix padding
    m = len(s) % 4
    if m != 0:
        s += '=' * (4 - m)
    data = base64.b64decode(s)
    subformat = kwargs.pop('subformat', None)
    encoding = kwargs.pop('encoding', 'utf-8' if subformat else None)
    if encoding:
        data = data.decode(encoding)
        if subformat:
            decode_func = _get_format_decoder(subformat)
            if decode_func:
                data = decode_func(data, **kwargs)
    return data


def decode_csv(s, **kwargs):
    # kwargs.setdefault('delimiter', ',')
    if kwargs.pop('quote', False):
        kwargs.setdefault('quoting', csv.QUOTE_ALL)
    columns = kwargs.pop('columns', None)
    columns_row = kwargs.pop('columns_row', True)
    f = StringIO(s)
    r = csv.reader(f, **kwargs)
    ln = 0
    data = []
    for row in r:
        if ln == 0 and columns_row:
            if not columns:
                columns = row
            ln += 1
            continue
        d = dict(zip(columns, row))
        data.append(d)
        ln += 1
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


def encode(d, format, **kwargs):
    encode_func = _get_format_encoder(format)
    if encode_func:
        s = encode_func(d, **kwargs)
        return s
    else:
        raise ValueError('Invalid format: {}.'.format(format))


def encode_base64(d, **kwargs):
    data = d
    subformat = kwargs.pop('subformat', None)
    encoding = kwargs.pop('encoding', 'utf-8' if subformat else None)
    if not isinstance(data, string_types) and subformat:
        encode_func = _get_format_encoder(subformat)
        if encode_func:
            data = encode_func(data, **kwargs)
    if isinstance(data, string_types) and encoding:
        data = data.encode(encoding)
    data = base64.b64encode(data)
    if isinstance(data, binary_type) and encoding:
        data = data.decode(encoding)
    return data


def encode_csv(l, **kwargs):
    # kwargs.setdefault('delimiter', ',')
    if kwargs.pop('quote', False):
        kwargs.setdefault('quoting', csv.QUOTE_ALL)
    kwargs.setdefault('lineterminator', '\n')
    columns = kwargs.pop('columns', None)
    columns_row = kwargs.pop('columns_row', True)
    if not columns and len(l) and isinstance(l[0], dict):
        keys = [str(key) for key in l[0].keys()]
        columns = list(sorted(keys))
    f = StringIO()
    w = csv.writer(f, **kwargs)
    if columns_row and columns:
        w.writerow(columns)
    for item in l:
        if isinstance(item, dict):
            row = [item.get(key, '') for key in columns]
        elif isinstance(item, (list, tuple, set, )):
            row = item
        else:
            row = [item]
        w.writerow(row)
    data = f.getvalue()
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


_formats = {
    'b64': {
        'decoder': decode_base64,
        'encoder': encode_base64,
    },
    'base64': {
        'decoder': decode_base64,
        'encoder': encode_base64,
    },
    'csv': {
        'decoder': decode_csv,
        'encoder': encode_csv,
    },
    'json': {
        'decoder': decode_json,
        'encoder': encode_json,
    },
    'qs': {
        'decoder': decode_query_string,
        'encoder': encode_query_string,
    },
    'query_string': {
        'decoder': decode_query_string,
        'encoder': encode_query_string,
    },
    'toml': {
        'decoder': decode_toml,
        'encoder': encode_toml,
    },
    'yaml': {
        'decoder': decode_yaml,
        'encoder': encode_yaml,
    },
    'yml': {
        'decoder': decode_yaml,
        'encoder': encode_yaml,
    },
    'xml': {
        'decoder': decode_xml,
        'encoder': encode_xml,
    },
}


def _get_format(format):
    return _formats.get(
        slugify(format, separator='_'), {})


def _get_format_decoder(format):
    return _get_format(format).get('decoder', None)


def _get_format_encoder(format):
    return _get_format(format).get('encoder', None)
