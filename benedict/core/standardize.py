# -*- coding: utf-8 -*-

from benedict.core.rename import rename
from benedict.core.traverse import traverse
from benedict.utils import type_util

from slugify import slugify

import re


def standardize(d):
    def standardize_item(item_dict, item_key, item_value):
        if type_util.is_string(item_key):
            # https://stackoverflow.com/a/12867228/2096218
            norm_key = re.sub(
                r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))', r'_\1', item_key)
            norm_key = slugify(norm_key, separator='_')
            rename(item_dict, item_key, norm_key)
    traverse(d, standardize_item)
