from benedict.exceptions import ExtrasRequireModuleNotFoundError


def _require_optional_module(*, installed, package, target):
    if not installed:
        raise ExtrasRequireModuleNotFoundError(
            package=package,
            target=target,
        )


def require_s3(*, installed):
    _require_optional_module(
        installed=installed,
        package="boto3",
        target="s3",
    )


def require_toml(*, installed):
    _require_optional_module(
        installed=installed,
        package="toml",
        target="toml",
    )


def require_xls(*, installed):
    _require_optional_module(
        installed=installed[0],
        package="openpyxl",
        target="xls",
    )
    _require_optional_module(
        installed=installed[1],
        package="xlrd",
        target="xls",
    )


def require_xml(*, installed):
    _require_optional_module(
        installed=installed,
        package="xmltodict",
        target="xml",
    )


def require_yaml(*, installed):
    _require_optional_module(
        installed=installed,
        package="pyyaml",
        target="yaml",
    )
