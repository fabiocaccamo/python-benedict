# -*- coding: utf-8 -*-

from benedict.serializers import (
    get_format_by_path, get_serializer_by_format, get_serializers_extensions, )

from six import PY2

import errno
import os
import requests


def autodetect_format(s):
    if is_url(s) or is_filepath(s):
        return get_format_by_path(s)
    return None


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError('Invalid format: {}.'.format(format))
    decode_opts = kwargs.copy()
    data = serializer.decode(s.strip(), **decode_opts)
    return data


def encode(d, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError('Invalid format: {}.'.format(format))
    s = serializer.encode(d, **kwargs)
    return s


def is_data(s):
    return (len(s.splitlines()) > 1)


def is_filepath(s):
    if any([s.endswith(ext) for ext in get_serializers_extensions()]):
        return True
    return os.path.isfile(s)


def is_url(s):
    return any([s.startswith(protocol)
                for protocol in ['http://', 'https://']])


def read_content(s):
    # s -> filepath or url or data
    if is_data(s):
        # data
        return s
    elif is_url(s):
        # url
        return read_url(s)
    elif is_filepath(s):
        # filepath
        return read_file(s)
    # one-line data?!
    return s


def read_file(filepath, encoding='utf-8'):
    if os.path.isfile(filepath):
        content = ''
        options = {} if PY2 else { 'encoding':encoding }
        with open(filepath, 'r', **options) as file:
            content = file.read()
        return content
    return None


def read_url(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    if response.status_code == requests.codes.ok:
        content = response.text
        return content
    raise ValueError(
        'Invalid url response status code: {}.'.format(
            response.status_code))


def write_file_dir(filepath):
    filedir = os.path.dirname(filepath)
    if os.path.exists(filedir):
        return
    try:
        os.makedirs(filedir)
    except OSError as e:
        # Guard against race condition
        if e.errno != errno.EEXIST:
            raise e


def write_file(filepath, content, encoding='utf-8'):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    write_file_dir(filepath)
    options = {} if PY2 else { 'encoding':encoding }
    with open(filepath, 'w+', **options) as file:
        file.write(content)
    return True
