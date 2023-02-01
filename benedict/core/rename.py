from benedict.core.move import move


def rename(d, key, key_new) -> None:
    move(d, key, key_new, overwrite=False)
