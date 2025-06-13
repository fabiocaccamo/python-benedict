from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from typing import Any, cast

from typing_extensions import TypeVar

from benedict.dicts.base import BaseDict
from benedict.dicts.parse import parse_util
from benedict.utils import type_util

_K = TypeVar("_K", default=str)
_V = TypeVar("_V", default=Any)

ParserFunc = Callable[..., Any]


class ParseDict(BaseDict[_K, _V]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Constructs a new instance.
        """
        super().__init__(*args, **kwargs)

    def _get_value(
        self,
        key: Any,
        default: Any,
        choices: Any,
        parser_func: ParserFunc,
        parserstrwargs: Any = None,
    ) -> Any:
        """
        Get value by key, or keypath core method.
        If choices and value is in choices return value otherwise default.
        """

        # Get raw value from self.
        value = self.get(key, None)
        # If value is None return default value.
        if value is None:
            return default

        # If not of the desired type, try to parse it using parser_func.
        value = parser_func(value, **(parserstrwargs or {}))
        # If value is None after parsing return default value.
        if value is None:
            return default

        # If choices and value in choices return value otherwise default.
        if (
            type_util.is_list_or_tuple(choices)
            and len(choices)
            and value not in choices
        ):
            return default

        return value

    def _get_values_list(
        self,
        key: _K,
        default: list[Any] | None,
        separator: str | None,
        parser_func: ParserFunc,
        parserstrwargs: Any = None,
    ) -> list[Any]:
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        if key not in self:
            return default or []
        values_list = self.get_list(key, [], separator)
        return [parser_func(value, **(parserstrwargs or {})) for value in values_list]

    def get_bool(self, key: _K, default: bool = False) -> bool:
        """
        Get value by key or keypath trying to return it as bool.
        Values like `1`, `true`, `yes`, `on` will be returned as `True`.
        """
        return cast(
            "bool", self._get_value(key, default, [True, False], parse_util.parse_bool)
        )

    def get_bool_list(
        self, key: _K, default: list[bool] | None = None, separator: str = ","
    ) -> list[bool]:
        """
        Get value by key or keypath trying to return it as list of bool values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(key, default, separator, parse_util.parse_bool)

    def get_date(
        self,
        key: _K,
        default: date | None = None,
        format: str | None = None,
        choices: Sequence[date] | None = None,
    ) -> date | None:
        """
        Get value by key or keypath trying to return it as date.
        If format is not specified it will be autodetected.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "date | None",
            self._get_value(
                key, default, choices, parse_util.parse_date, {"format": format}
            ),
        )

    def get_date_list(
        self,
        key: _K,
        default: Any = None,
        format: str | None = None,
        separator: str = ",",
    ) -> list[date]:
        """
        Get value by key or keypath trying to return it as list of date values.
        If separator is specified and value is a string it will be splitted.
        """
        return cast(
            "list[date]",
            self._get_values_list(
                key, default, separator, parse_util.parse_date, {"format": format}
            ),
        )

    def get_datetime(
        self,
        key: _K,
        default: datetime | None = None,
        format: str | None = None,
        choices: Sequence[datetime] | None = None,
    ) -> datetime | None:
        """
        Get value by key or keypath trying to return it as datetime.
        If format is not specified it will be autodetected.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "datetime | None",
            self._get_value(
                key, default, choices, parse_util.parse_datetime, {"format": format}
            ),
        )

    def get_datetime_list(
        self,
        key: _K,
        default: list[datetime] | None = None,
        format: str | None = None,
        separator: str = ",",
    ) -> list[datetime]:
        """
        Get value by key or keypath trying to return it as list of datetime values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(
            key, default, separator, parse_util.parse_datetime, {"format": format}
        )

    def get_decimal(
        self,
        key: _V,
        default: Decimal | None = Decimal("0.0"),
        choices: Sequence[Decimal] | None = None,
    ) -> Decimal:  # noqa: B008
        """
        Get value by key or keypath trying to return it as Decimal.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "Decimal",
            self._get_value(key, default, choices, parse_util.parse_decimal),
        )

    def get_decimal_list(
        self, key: _K, default: list[Decimal] | None = None, separator: str = ","
    ) -> list[Decimal]:
        """
        Get value by key or keypath trying to return it as list of Decimal values.
        If separator is specified and value is a string it will be splitted.
        """
        return cast(
            "list[Decimal]",
            self._get_values_list(key, default, separator, parse_util.parse_decimal),
        )

    def get_dict(
        self, key: _K, default: Mapping[str, Any] | None = None
    ) -> dict[_K, Any]:
        """
        Get value by key or keypath trying to return it as dict.
        If value is a json string it will be automatically decoded.
        """
        return cast(
            "dict[_K, Any]",
            self._get_value(key, default or {}, None, parse_util.parse_dict),
        )

    def get_email(
        self,
        key: _K,
        default: str = "",
        choices: Sequence[str] | None = None,
        check_blacklist: bool = True,
    ) -> str:
        """
        Get email by key or keypath and return it.
        If value is blacklisted it will be automatically ignored.
        If check_blacklist is False, it will be not ignored even if blacklisted.
        """
        return cast(
            "str",
            self._get_value(
                key,
                default,
                choices,
                parse_util.parse_email,
                {"check_blacklist": check_blacklist},
            ),
        )

    def get_float(
        self, key: _K, default: float = 0.0, choices: Sequence[_V] | None = None
    ) -> float:
        """
        Get value by key or keypath trying to return it as float.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "float",
            self._get_value(key, default, choices, parse_util.parse_float),
        )

    def get_float_list(
        self, key: _K, default: list[float] | None = None, separator: str = ","
    ) -> list[float]:
        """
        Get value by key or keypath trying to return it as list of float values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(key, default, separator, parse_util.parse_float)

    def get_int(
        self, key: _K, default: int = 0, choices: Sequence[int] | None = None
    ) -> int:
        """
        Get value by key or keypath trying to return it as int.
        If choices and value is in choices return value otherwise default.
        """
        return cast("int", self._get_value(key, default, choices, parse_util.parse_int))

    def get_int_list(
        self, key: _K, default: list[int] | None = None, separator: str = ","
    ) -> list[int] | None:
        """
        Get value by key or keypath trying to return it as list of int values.
        If separator is specified and value is a string it will be splitted.
        """
        return cast(
            "list[int]",
            self._get_values_list(key, default, separator, parse_util.parse_int),
        )

    def get_list(
        self,
        key: _K,
        default: Sequence[Any] | None = None,
        separator: str | None = ",",
    ) -> list[Any]:
        """
        Get value by key or keypath trying to return it as list.
        If separator is specified and value is a string it will be splitted.
        """
        return cast(
            "list[Any]",
            self._get_value(
                key,
                default or [],
                None,
                parse_util.parse_list,
                {"separator": separator},
            ),
        )

    def get_list_item(
        self, key: _K, index: int = 0, default: Any = None, separator: str = ","
    ) -> Any:
        """
        Get list by key or keypath and return value at the specified index.
        If separator is specified and list value is a string it will be splitted.
        """
        values = self.get_list(key, None, separator)
        if values:
            try:
                value = values[index]
                return value
            except IndexError:
                return default
        else:
            return default

    def get_phonenumber(
        self,
        key: _K,
        country_code: str | None = None,
        default: dict[str, str] | None = None,
    ) -> dict[str, str] | None:
        """
        Get phonenumber by key or keypath and return a dict
        with different formats (e164, international, national).
        If country code is specified (alpha 2 code),
        it will be used to parse phone number correctly.
        """
        return cast(
            "dict[str, str]",
            self._get_value(
                key,
                default or {},
                None,
                parse_util.parse_phonenumber,
                {"country_code": country_code},
            ),
        )

    def get_slug(
        self, key: _K, default: str = "", choices: Sequence[str] | None = None
    ) -> str:
        """
        Get value by key or keypath trying to return it as slug.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "str", self._get_value(key, default, choices, parse_util.parse_slug)
        )

    def get_slug_list(
        self, key: _K, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """
        Get value by key or keypath trying to return it as list of slug values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(key, default, separator, parse_util.parse_slug)

    def get_str(
        self, key: _K, default: str = "", choices: Sequence[str] | None = None
    ) -> str:
        """
        Get value by key or keypath trying to return it as string.
        Encoding issues will be automatically fixed.
        If choices and value is in choices return value otherwise default.
        """
        return cast("str", self._get_value(key, default, choices, parse_util.parse_str))

    def get_str_list(
        self, key: _K, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """
        Get value by key or keypath trying to return it as list of str values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(key, default, separator, parse_util.parse_str)

    def get_uuid(
        self, key: _K, default: str = "", choices: Sequence[str] | None = None
    ) -> str:
        """
        Get value by key or keypath trying to return it as valid uuid.
        If choices and value is in choices return value otherwise default.
        """
        return cast(
            "str", self._get_value(key, default, choices, parse_util.parse_uuid)
        )

    def get_uuid_list(
        self, key: _K, default: list[str] | None = None, separator: str = ","
    ) -> list[str]:
        """
        Get value by key or keypath trying to return it as list of valid uuid values.
        If separator is specified and value is a string it will be splitted.
        """
        return self._get_values_list(key, default, separator, parse_util.parse_uuid)
