import copy
from typing import Any, Dict, Optional


def clone(obj, empty: bool = False, memo: Optional[Dict[int, Any]] = None):
    d = copy.deepcopy(obj, memo)
    if empty:
        d.clear()
    return d
