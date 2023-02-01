import re
from typing import Any
from urllib.parse import parse_qs, urlencode

from benedict.serializers.abstract import AbstractSerializer


class QueryStringSerializer(AbstractSerializer):
    """
    This class describes a query-string serializer.
    """

    def __init__(self):
        super().__init__(
            extensions=[
                "qs",
                "querystring",
            ],
        )

    def decode(self, s: str, **kwargs: Any):
        flat = kwargs.pop("flat", True)
        qs_re = r"(?:([\w\-\%\+\.\|]+\=[\w\-\%\+\.\|]*)+(?:[\&]{1})?)+"
        qs_pattern = re.compile(qs_re)
        if qs_pattern.match(s):
            qs_data = parse_qs(s)
            if flat:
                data = {key: value[0] for key, value in qs_data.items()}
            return data
        raise ValueError(f"Invalid query string: {s}")

    def encode(self, d, **kwargs: Any) -> str:
        data = urlencode(d, **kwargs)
        return data
