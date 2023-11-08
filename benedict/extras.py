from benedict.exceptions import ExtrasRequireModuleNotFoundError

__all__ = [
    "require_html",
    "require_parse",
    "require_s3",
    "require_toml",
    "require_xls",
    "require_xml",
    "require_yaml",
]


def _require_optional_dependencies(*, target, installed):
    if not installed:
        raise ExtrasRequireModuleNotFoundError(target=target)


def require_html(*, installed):
    _require_optional_dependencies(target="html", installed=installed)


def require_parse(*, installed):
    _require_optional_dependencies(target="parse", installed=installed)


def require_s3(*, installed):
    _require_optional_dependencies(target="s3", installed=installed)


def require_toml(*, installed):
    _require_optional_dependencies(target="toml", installed=installed)


def require_xls(*, installed):
    _require_optional_dependencies(target="xls", installed=installed)


def require_xml(*, installed):
    _require_optional_dependencies(target="xml", installed=installed)


def require_yaml(*, installed):
    _require_optional_dependencies(target="yaml", installed=installed)
