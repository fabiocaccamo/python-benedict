# -*- coding: utf-8 -*-

import errno
import json
import os
import requests
import yaml


def decode_json(s, **kwargs):
    data = json.loads(s, **kwargs)
    return data


def decode_yaml(s, **kwargs):
    kwargs.setdefault('Loader', yaml.Loader)
    data = yaml.load(s, **kwargs)
    return data


def encode_json(d, **kwargs):
    data = json.dumps(d, **kwargs)
    return data


def encode_yaml(d, **kwargs):
    data = yaml.dump(d, **kwargs)
    return data


def read_file(filepath):
    handler = open(filepath, 'r')
    content = handler.read()
    handler.close()
    return content


def read_url(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    content = response.text
    return content


def write_file(filepath, content):
    # https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as e:
            # Guard against race condition
            if e.errno != errno.EEXIST:
                raise e
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
