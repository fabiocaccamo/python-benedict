# -*- coding: utf-8 -*-

from benedict.core.move import move


def rename(d, key, key_new):
    move(d, key, key_new, overwrite=False)
