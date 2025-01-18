from benedict.core.keylists import keylists
from benedict.utils import type_util


def keypaths(d, separator=".", indexes=False, sort=True):
    separator = separator or "."
    if not type_util.is_string(separator):
        raise ValueError("separator argument must be a (non-empty) string.")
    kls = keylists(d, indexes=indexes)
    kps = [separator.join([f"{key}" for key in kl]) for kl in kls]
    if sort:
        kps.sort()
    return kps
