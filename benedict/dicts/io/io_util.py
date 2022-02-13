# -*- coding: utf-8 -*-

from benedict.serializers import (
    get_format_by_path,
    get_serializer_by_format,
    get_serializers_extensions,
)

import fsutil


def autodetect_format(s):
    if is_url(s) or is_filepath(s):
        return get_format_by_path(s)
    return None


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError("Invalid format: {}.".format(format))
    decode_opts = kwargs.copy()
    data = serializer.decode(s.strip(), **decode_opts)
    return data


def encode(d, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError("Invalid format: {}.".format(format))
    s = serializer.encode(d, **kwargs)
    return s


def is_data(s):
    return len(s.splitlines()) > 1


def is_filepath(s):
    if any([s.endswith(ext) for ext in get_serializers_extensions()]):
        return True
    return fsutil.is_file(s)


def is_url(s):
    return any([s.startswith(protocol) for protocol in ["http://", "https://"]])


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


def read_file(filepath, **options):
    if fsutil.is_file(filepath):
        return fsutil.read_file(filepath, **options)
    return None


def read_url(url, **options):
    return fsutil.read_file_from_url(url, **options)


def write_file(filepath, content, **options):
    fsutil.write_file(filepath, content, **options)
