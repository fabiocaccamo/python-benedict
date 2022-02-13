# -*- coding: utf-8 -*-


def move(d, key_src, key_dest, overwrite=True):
    if key_dest == key_src:
        return
    if key_dest in d and not overwrite:
        raise KeyError(
            "Invalid key: '{}', key already in target dict "
            "and `overwrite` is disabled.".format(key_dest)
        )
    d[key_dest] = d.pop(key_src)
