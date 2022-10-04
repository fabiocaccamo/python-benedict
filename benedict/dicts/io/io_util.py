# -*- coding: utf-8 -*-

from benedict.serializers import (
    get_format_by_path,
    get_serializer_by_format,
    get_serializers_extensions,
)

import fsutil
import s3fs

# try:
#     import s3fs
#     _s3fs_available = True
# except ImportError:
#     _s3fs_available = False
#
# # TODO: move to exceptions module
# try:
#     LibraryNotInstalledError = ModuleNotFoundError
# except NameError:
#     # python < 3.6
#     LibraryNotInstalledError = ImportError


def _get_s3_file_system(**options):
    # if not _s3fs_available:
    #     raise LibraryNotInstalledError(
    #         'Optional library module \'s3fs\' was not found. ' \
    #         'This can be solved by running: \'pip install python-benedict[s3]\''
    #     )
    fs = s3fs.S3FileSystem(**options)
    return fs


def autodetect_format(s):
    if any([is_url(s), is_s3_filepath(s), is_filepath(s)]):
        return get_format_by_path(s)
    return None


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    decode_opts = kwargs.copy()
    data = serializer.decode(s.strip(), **decode_opts)
    return data


def encode(d, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    s = serializer.encode(d, **kwargs)
    return s


def _is_supported_file_extension(s):
    return any([s.lower().endswith(ext) for ext in get_serializers_extensions()])


def is_data(s):
    return len(s.splitlines()) > 1


def is_filepath(s):
    return _is_supported_file_extension(s) or fsutil.is_file(s)


def is_s3_filepath(s):
    return s.startswith("s3://") and _is_supported_file_extension(s)


def is_url(s):
    return any([s.startswith(protocol) for protocol in ["http://", "https://"]])


def read_content(s, **options):
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
    elif is_s3_filepath(s):
        # s3 filepath
        s3_options = options.pop("s3_options", {})
        return read_file_from_s3(s, **s3_options)
    # one-line data?!
    return s


def read_file(filepath, **options):
    if is_s3_filepath(filepath):
        return read_file_from_s3(**options)
    elif fsutil.is_file(filepath):
        return fsutil.read_file(filepath, **options)
    return None


def read_file_from_s3(filepath, **options):
    options.setdefault("default_cache_type", "none")
    fs = _get_s3_file_system(**options)
    with fs.open(filepath, "r") as file:
        return file.read()
    return None


def read_url(url, **options):
    return fsutil.read_file_from_url(url, **options)


def write_file(filepath, content, **options):
    if is_s3_filepath(filepath):
        write_file_to_s3(filepath, content, **options)
    else:
        fsutil.write_file(filepath, content, **options)


def write_file_to_s3(filepath, content, **options):
    fs = _get_s3_file_system(**options)
    with fs.open(filepath) as file:
        file.write(content.encode("utf-8"))
