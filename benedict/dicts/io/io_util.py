import tempfile

# from botocore.exceptions import ClientError
from urllib.parse import urlparse

import boto3
import fsutil

from benedict.serializers import get_format_by_path, get_serializer_by_format


def autodetect_format(s):
    if any([is_url(s), is_s3(s), is_filepath(s)]):
        return get_format_by_path(s)
    return None


def decode(s, format, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    options = kwargs.copy()
    if format in ["b64", "base64"]:
        options.setdefault("subformat", "json")
    content = read_content(s, format, options)
    data = serializer.decode(content, **options)
    return data


def encode(d, format, filepath=None, **kwargs):
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    options = kwargs.copy()
    content = serializer.encode(d, **options)
    if filepath:
        write_content(filepath, content, **options)
    return content


def is_binary_format(format):
    return format in [
        "xls",
        "xlsx",
        "xlsm",
    ]


def is_data(s):
    return len(s.splitlines()) > 1


def is_filepath(s):
    return fsutil.is_file(s) or get_format_by_path(s)


def is_s3(s):
    return s.startswith("s3://") and get_format_by_path(s)


def is_url(s):
    return any([s.startswith(protocol) for protocol in ["http://", "https://"]])


def parse_s3_url(url):
    parsed = urlparse(url, allow_fragments=False)
    bucket = parsed.netloc
    key = parsed.path.lstrip("/")
    if parsed.query:
        key += "?" + parsed.query
    url = parsed.geturl()
    return {
        "url": url,
        "bucket": bucket,
        "key": key,
    }


def read_content(s, format=None, options=None):
    # s -> filepath or url or data
    # options.setdefault("format", format)
    options = options or {}
    s = s.strip()
    if is_data(s):
        return s
    elif is_url(s):
        requests_options = options.pop("requests_options", None) or {}
        return read_content_from_url(s, requests_options, format)
    elif is_s3(s):
        s3_options = options.pop("s3_options", None) or {}
        return read_content_from_s3(s, s3_options, format)
    elif is_filepath(s):
        return read_content_from_file(s, format)
    # one-line data?!
    return s


def read_content_from_file(filepath, format=None):
    binary_format = is_binary_format(format)
    if binary_format:
        return filepath
    return fsutil.read_file(filepath)


def read_content_from_s3(url, s3_options, format=None):
    s3_url = parse_s3_url(url)
    dirpath = tempfile.gettempdir()
    filename = fsutil.get_filename(s3_url["key"])
    filepath = fsutil.join_path(dirpath, filename)
    s3 = boto3.client("s3", **s3_options)
    s3.download_file(s3_url["bucket"], s3_url["key"], filepath)
    s3.close()
    content = read_content_from_file(filepath, format)
    return content


def read_content_from_url(url, requests_options, format=None):
    binary_format = is_binary_format(format)
    if binary_format:
        dirpath = tempfile.gettempdir()
        filepath = fsutil.download_file(url, dirpath, **requests_options)
        return filepath
    return fsutil.read_file_from_url(url, **requests_options)


def write_content(filepath, content, **options):
    if is_s3(filepath):
        write_content_to_s3(filepath, content, **options)
    else:
        write_content_to_file(filepath, content, **options)


def write_content_to_file(filepath, content, **options):
    fsutil.write_file(filepath, content)


def write_content_to_s3(url, content, s3_options, **options):
    s3_url = parse_s3_url(url)
    dirpath = tempfile.gettempdir()
    filename = fsutil.get_filename(s3_url["key"])
    filepath = fsutil.join_path(dirpath, filename)
    fsutil.write_file(filepath, content)
    s3 = boto3.client("s3", **s3_options)
    s3.upload_file(filepath, s3_url["bucket"], s3_url["key"])
    s3.close()
    fsutil.remove_file(filepath)
