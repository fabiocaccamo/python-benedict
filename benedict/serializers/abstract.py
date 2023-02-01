from typing import Any, List, Optional


class AbstractSerializer:
    """
    This class describes an abstract serializer.
    """

    def __init__(self, extensions: Optional[List[str]] = None):
        super().__init__()
        self._extensions = (extensions or []).copy()

    def decode(self, s: str, **kwargs: Any):
        raise NotImplementedError()

    def encode(self, d, **kwargs: Any) -> str:
        raise NotImplementedError()

    def extensions(self) -> List[str]:
        return self._extensions.copy()
