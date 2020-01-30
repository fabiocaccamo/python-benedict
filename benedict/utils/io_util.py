# -*- coding: utf-8 -*-

from benedict.serializers import (
    get_serializer_by_format, get_serializers_extensions, )

import errno
import os
import requests


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if serializer:
        decode_opts = kwargs.copy()
        data = serializer.decode(s.strip(), **decode_opts)
        return data
    raise ValueError('Invalid format: {}.'.format(format))


def encode(d, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if serializer:
        s = serializer.encode(d, **kwargs)
        return s
    raise ValueError('Invalid format: {}.'.format(format))


def read_content(s):
    # s -> filepath or url or data
    num_lines = len(s.splitlines())
    if num_lines > 1:
        # data
        return s
    if any([s.startswith(protocol)
            for protocol in ['http://', 'https://']]):
        # url
        return read_url(s)
    elif any([s.endswith(extension)
              for extension in get_serializers_extensions()]):
        # filepath
        if os.path.isfile(s):
            return read_file(s)
        return None
    return s


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


def write_file(filepath, content):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    write_file_dir(filepath)
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
