# -*- coding: utf-8 -*-

from benedict.serializers import (
    get_format_by_path,
    get_serializer_by_format,
    get_serializers_extensions,
)

import fsutil
import tempfile


def autodetect_format(s):
    if is_url(s) or is_filepath(s):
        return get_format_by_path(s)
    return None


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    decode_opts = kwargs.copy()
    if format in ["b64", "base64"]:
        decode_opts.setdefault("subformat", "json")
    content = read_content(s, format)
    data = serializer.decode(content, **decode_opts)
    return data


def encode(d, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    s = serializer.encode(d, **kwargs)
    return s


def is_binary_format(format):
    return format in [
        "xls",
        "xlsx",
        "xlsm",
    ]


def is_data(s):
    return len(s.splitlines()) > 1


def is_filepath(s):
    if any([s.endswith(ext) for ext in get_serializers_extensions()]):
        return True
    return fsutil.is_file(s)


def is_url(s):
    return any([s.startswith(protocol) for protocol in ["http://", "https://"]])


def read_content(s, format):
    # s -> filepath or url or data
    s = s.strip()
    if is_data(s):
        return s
    elif is_url(s):
        return read_content_from_url(s, format)
    elif is_filepath(s):
        return read_content_from_file(s, format)
    # one-line data?!
    return s


def read_content_from_file(filepath, format):
    binary_format = is_binary_format(format)
    if binary_format:
        return filepath
    return read_file(filepath)


def read_content_from_url(url, format, **options):
    binary_format = is_binary_format(format)
    if binary_format:
        dirpath = tempfile.gettempdir()
        filepath = fsutil.download_file(url, dirpath, **options)
        return filepath
    return read_url(url, **options)


def read_file(filepath, **options):
    return fsutil.read_file(filepath, **options)


def read_url(url, **options):
    return fsutil.read_file_from_url(url, **options)


def write_file(filepath, content, **options):
    fsutil.write_file(filepath, content, **options)
