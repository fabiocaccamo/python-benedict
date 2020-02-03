# -*- coding: utf-8 -*-

from benedict.utils import type_util

import json


def dump(data):
    def encoder(obj):
        if not type_util.is_json_serializable(obj):
            return str(obj)
    return json.dumps(data, indent=4, sort_keys=True, default=encoder)
