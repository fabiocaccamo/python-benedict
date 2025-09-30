import base64
import pickle
from typing import Any

from typing_extensions import override

from benedict.serializers.abstract import AbstractSerializer


class PickleSerializer(AbstractSerializer[str, Any]):
    """
    This class describes a pickle serializer.
    """

    @override
    def __init__(self) -> None:
        super().__init__(
            extensions=[
                "pickle",
            ],
        )

    @override
    def decode(self, s: str, **kwargs: Any) -> Any:
        encoding = kwargs.pop("encoding", "utf-8")
        return pickle.loads(base64.b64decode(s.encode(encoding)), **kwargs)

    @override
    def encode(self, d: Any, **kwargs: Any) -> str:
        encoding = kwargs.pop("encoding", "utf-8")
        kwargs.setdefault("protocol", 2)
        return base64.b64encode(pickle.dumps(d, **kwargs)).decode(encoding)
