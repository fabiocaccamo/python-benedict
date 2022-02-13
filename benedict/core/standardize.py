# -*- coding: utf-8 -*-

from benedict.core.rename import rename
from benedict.core.traverse import traverse
from benedict.utils import type_util

from slugify import slugify

import re


def _standardize_item(d, key, value):
    if type_util.is_string(key):
        # https://stackoverflow.com/a/12867228/2096218
        norm_key = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", key)
        norm_key = slugify(norm_key, separator="_")
        rename(d, key, norm_key)


def standardize(d):
    traverse(d, _standardize_item)
