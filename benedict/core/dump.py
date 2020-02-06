# -*- coding: utf-8 -*-

from benedict.utils import type_util
from six import text_type

import json


def _encoder(obj):
    if not type_util.is_json_serializable(obj):
        return text_type(obj)


def dump(obj, **kwargs):
    options = {
        'indent': 4,
        'sort_keys': True,
        'default': _encoder,
    }
    options.update(**kwargs)
    try:
        output = json.dumps(obj, **options)
    except TypeError:
        options['sort_keys'] = False
        output = json.dumps(obj, **options)
    return output
