def _clean_dict(d, strings, collections):
    keys = list(d.keys())
    for key in keys:
        d[key] = _clean_value(d[key], strings=strings, collections=collections)
        if d[key] is None:
            del d[key]
    return d


def _clean_list(ls, strings, collections):
    for i in range(len(ls) - 1, -1, -1):
        ls[i] = _clean_value(ls[i], strings=strings, collections=collections)
        if ls[i] is None:
            ls.pop(i)
    return ls


def _clean_set(values, strings, collections):
    return {
        value
        for value in values
        if _clean_value(value, strings=strings, collections=collections) is not None
    }


def _clean_str(s, strings, collections):
    return s if s and s.strip() else None


def _clean_tuple(values, strings, collections):
    return tuple(
        value
        for value in values
        if _clean_value(value, strings=strings, collections=collections) is not None
    )


def _clean_value(value, strings, collections):
    if value is None:
        return value
    elif isinstance(value, list) and collections:
        value = _clean_list(value, strings=strings, collections=collections) or None
    elif isinstance(value, dict) and collections:
        value = _clean_dict(value, strings=strings, collections=collections) or None
    elif isinstance(value, set) and collections:
        value = _clean_set(value, strings=strings, collections=collections) or None
    elif isinstance(value, str) and strings:
        value = _clean_str(value, strings=strings, collections=collections) or None
    elif isinstance(value, tuple) and collections:
        value = _clean_tuple(value, strings=strings, collections=collections) or None
    return value


def clean(d, strings=True, collections=True):
    return _clean_dict(d, strings=strings, collections=collections)
