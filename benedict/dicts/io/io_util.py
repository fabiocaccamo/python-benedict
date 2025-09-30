from __future__ import annotations

import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path

# from botocore.exceptions import ClientError
from typing import Any, cast
from urllib.parse import urlparse

try:
    import boto3

    s3_installed = True
except ModuleNotFoundError:
    s3_installed = False

import fsutil

from benedict.extras import require_s3
from benedict.serializers import (
    get_format_by_path,
    get_serializer_by_format,
)
from benedict.utils import type_util


def autodetect_format(s: Any) -> str | None:
    s = str(s)
    if any([is_url(s), is_s3(s), is_filepath(s)]):
        return get_format_by_path(s)
    return None


def check_source(source: str, allowed_sources: str | Sequence[Any]) -> None:
    # enforce allowed_sources to be a list of strings
    if not allowed_sources:
        allowed_sources = ["*"]
    elif type_util.is_string(allowed_sources):
        allowed_sources = [allowed_sources]
    elif type_util.is_list_or_tuple(allowed_sources):
        allowed_sources = list(allowed_sources)
    # check if any "all" marker is present
    all_sources = ["*", "all", "auto"]
    for source_item in all_sources:
        if source_item in allowed_sources:
            # all sources
            return
    if source not in allowed_sources:
        raise ValueError(f"Invalid source: '{source}' (source not allowed).")


def decode(s: Any, format: str, **kwargs: Any) -> Any:
    s = str(s)
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    options = kwargs.copy()
    if format in ["b64", "base64"]:
        options.setdefault("subformat", "json")
    content = read_content(s, format, options)
    data = serializer.decode(content, **options)
    return data


def encode(d: Any, format: str, filepath: str | None = None, **kwargs: Any) -> Any:
    serializer = get_serializer_by_format(format)
    if not serializer:
        raise ValueError(f"Invalid format: {format}.")
    options = kwargs.copy()
    content = serializer.encode(d, **options)
    if filepath:
        filepath = str(filepath)
        write_content(filepath, content, **options)
    return content


def is_binary_format(format: str | None) -> bool:
    return format in [
        "xls",
        "xlsx",
        "xlsm",
    ]


def is_data(s: str | bytes) -> bool:
    return len(s.splitlines()) > 1


def is_filepath(s: Path | str) -> bool:
    if fsutil.is_file(s):
        return True
    return bool(
        get_format_by_path(s)
        and not is_data(cast("str", s))
        and not is_s3(cast("str", s))
        and not is_url(cast("str", s))
    )


def is_s3(s: str) -> bool:
    return s.startswith("s3://")


def is_url(s: str) -> bool:
    return any(s.startswith(protocol) for protocol in ["http://", "https://"])


def parse_s3_url(url: str) -> dict[str, str]:
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


def read_content(
    s: str, format: str | None = None, options: dict[str, Any] | None = None
) -> str:
    # s -> filepath or url or data
    # options.setdefault("format", format)
    options = options or {}
    sources = options.pop("sources", None)
    s = s.strip()
    if is_data(s):
        check_source("data", allowed_sources=sources)
        return s
    elif is_url(s):
        check_source("url", allowed_sources=sources)
        requests_options = options.pop("requests_options", None) or {}
        return read_content_from_url(s, requests_options, format)
    elif is_s3(s):
        check_source("s3", allowed_sources=sources)
        s3_options = options.pop("s3_options", None) or {}
        return read_content_from_s3(s, s3_options, format)
    elif is_filepath(s):
        check_source("file", allowed_sources=sources)
        return read_content_from_file(s, format)
    # one-line data?!
    return s


def read_content_from_file(filepath: str, format: str | None = None) -> str:
    binary_format = is_binary_format(format)
    if binary_format:
        return filepath
    return fsutil.read_file(filepath)  # type: ignore[no-any-return]


def read_content_from_s3(
    url: str, s3_options: Mapping[str, Any], format: str | None = None
) -> str:
    require_s3(installed=s3_installed)
    s3_url = parse_s3_url(url)
    dirpath = tempfile.gettempdir()
    filename = fsutil.get_filename(s3_url["key"])
    filepath = fsutil.join_path(dirpath, filename)
    s3 = boto3.client("s3", **s3_options)
    s3.download_file(s3_url["bucket"], s3_url["key"], filepath)
    s3.close()
    content = read_content_from_file(filepath, format)
    return content


def read_content_from_url(
    url: str, requests_options: Mapping[str, Any], format: str | None = None
) -> str:
    binary_format = is_binary_format(format)
    if binary_format:
        dirpath = tempfile.gettempdir()
        filepath = fsutil.download_file(url, dirpath=dirpath, **requests_options)
        return filepath  # type: ignore[no-any-return]
    return fsutil.read_file_from_url(url, **requests_options)  # type: ignore[no-any-return]


def write_content(filepath: str, content: str, **options: Any) -> None:
    if is_s3(filepath):
        write_content_to_s3(filepath, content, **options)
    else:
        write_content_to_file(filepath, content, **options)


def write_content_to_file(filepath: str, content: str, **options: Any) -> None:
    fsutil.write_file(filepath, content)


def write_content_to_s3(
    url: str, content: str, s3_options: Mapping[str, Any], **options: Any
) -> None:
    require_s3(installed=s3_installed)
    s3_url = parse_s3_url(url)
    dirpath = tempfile.gettempdir()
    filename = fsutil.get_filename(s3_url["key"])
    filepath = fsutil.join_path(dirpath, filename)
    fsutil.write_file(filepath, content)
    s3 = boto3.client("s3", **s3_options)
    s3.upload_file(filepath, s3_url["bucket"], s3_url["key"])
    s3.close()
    fsutil.remove_file(filepath)
