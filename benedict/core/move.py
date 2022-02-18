# -*- coding: utf-8 -*-


def move(d, key_src, key_dest, overwrite=True):
    if key_dest == key_src:
        return
    if key_dest in d and not overwrite:
        raise KeyError(
            f"Invalid key: '{key_dest}', key already in target dict and 'overwrite' is disabled."
        )
    d[key_dest] = d.pop(key_src)
