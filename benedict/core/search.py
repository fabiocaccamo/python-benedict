from benedict.core.traverse import traverse
from benedict.utils import type_util


def _get_term(value, case_sensitive: bool):
    v_is_str = type_util.is_string(value)
    v = value.lower() if (v_is_str and not case_sensitive) else value
    return (v, v_is_str)


def _get_match(query, value, exact: bool, case_sensitive: bool) -> bool:
    q, q_is_str = _get_term(query, case_sensitive)
    v, v_is_str = _get_term(value, case_sensitive)
    # TODO: add regex support
    if q_is_str and v_is_str and not exact:
        return q in v
    return q == v


def search(
    d,
    query,
    in_keys: bool = True,
    in_values: bool = True,
    exact: bool = False,
    case_sensitive: bool = True,
):
    items = []

    def _search_item(item_dict, item_key, item_value):
        match_key = in_keys and _get_match(query, item_key, exact, case_sensitive)
        match_val = in_values and _get_match(query, item_value, exact, case_sensitive)
        if any([match_key, match_val]):
            items.append((item_dict, item_key, item_value))

    traverse(d, _search_item)
    return items
