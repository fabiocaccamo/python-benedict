# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.18.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.18.1) - 2020-03-13
-   Added data format auto-detection when creating instance with data from filepath or url.
-   Fixed `keypath_separator` support when using `from_{format}` methods.

## [0.18.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.18.0) - 2020-02-21
-   Added `from_pickle` and `to_pickle` methods.
-   Added `PickleSerializer`.
-   Added `datetime`, `Decimal` and `set` support to `JSONSerializer`.
-   Updated `dump` method to use `JSONSerializer`.
-   Refactored `Base64Serializer`.
-   Fixed `type_util.is_json_serializable` with `set` objects.
-   Fixed `search` method for int no results - #7
-   Improved `invert` method to handles correctly lists and tuples.
-   Improved `io_util.read_file` and `io_util.write_file methods`.
-   Improved code quality and CI.

## [0.17.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.17.0) - 2020-02-06
-   Added `groupby` utility method.
-   Added `nest` utility method.
-   Added `keylists` core method.
-   Reorganized lib and tests packages.
-   Improved code quality and CI.

## [0.16.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.16.0) - 2020-01-30
-   Added `KeylistDict` with list indexes support. #1
-   Added `benedict.utils.type_util` with many utility functions.
-   Improved code quality and CI.

## [0.15.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.15.0) - 2020-01-13
-   Added `rename` method.
-   Added `search` method.
-   Added `unflatten` method.

## [0.14.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.14.1) - 2020-01-07
-   Fixed `keypath_separator` value in instances returned by `copy`, `clone`, `filter`, `flatten`, `invert`, `subset` methods. #4
-   Fixed `get` doesn't work when the key is a list with one element. #5
-   Fixed `pickle` `AttributeError`. #6

## [0.14.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.14.0) - 2019-12-18
-   Added docstrings to methods. #2
-   Added test case for stackoverflow answered questions.
-   Added possibility to run tests using only `unittest`.
-   Improved code quality and CI.
-   Improved keypath support in `fromkeys` method.
-   Improved url, file, data autodetect in `io_util.read_content`.
-   Refactored `standardize` utility method.
-   Removed duplicated code and `benedicton` decorator.
-   Renamed `options` arg to `choices` in `ParseDict` methods.
-   Replaced unsafe `yaml.load` with `yaml.safe_load`.

## [0.13.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.13.0) - 2019-11-07
-   Added `csv` I/O support.
-   Refactored I/O dict class and utils.
-   Improved tests.

## [0.12.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.12.0) - 2019-10-29
-   Added `standardize` utility method.
-   Added `traverse` utility method.
-   Added `keypath_separator` getter/setter.
-   Improved `base64` I/O support.
-   Improved tests.
-   Refactored `benedict` class and utilies.

## [0.11.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.11.1) - 2019-10-14
-   Added `io_util.decode_bytes` utility method.

## [0.11.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.11.0) - 2019-10-14
-   Added `query-string` I/O support.
-   Added `unique` utility method.
-   Added urldecode, padding fix and `format=None` support to `io_util.decode_base64` utility.
-   Refactored `benedict` class and utilies.

## [0.10.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.10.0) - 2019-10-03
-   Added `base64` I/O support.
-   Added `invert` utility method.
-   Added `items_sorted_by_keys` utility method.
-   Added `items_sorted_by_values` utility method.
-   Refactored `benedict` class and utilies.

## [0.9.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.9.0) - 2019-09-23
-   Added `xml` I/O support.

## [0.8.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.8.0) - 2019-09-20
-   Added `toml` I/O support.

## [0.7.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.7.0) - 2019-09-17
-   Added `yaml` I/O support.

## [0.6.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.6.0) - 2019-09-10
-   Added `IODict` with `json` support.
-   Added `clone` (`deepcopy` alias) and `merge` (`deepupdate` alias) methods.

## [0.5.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.5.2) - 2019-07-19
-   Refactored `KeypathDict`.
-   Added `remove` utility method.
-   Added `subset` utility method.
-   Fixed string casting in parse functions on python 2.

## [0.5.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.5.1) - 2019-07-10
-   Added timestamp support to get_datetime parse method.

## [0.5.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.5.0) - 2019-07-09
-   Added custom or `None` keypath `separator` support.
-   Added `filter` utility method.
-   Improved tests and code quality.

## [0.4.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.4.2) - 2019-06-19
-   Fixed `parse_str` UnicodeEncodeError on python 2.

## [0.4.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.4.1) - 2019-06-18
-   Fixed `get_phonenumber` not working with numbers without country prefix.
-   Renamed `country` arg to `country_code` in `get_phonenumber` method.

## [0.4.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.4.0) - 2019-06-17
-   Added `clean` method.
-   Added `get_email` method.
-   Added `get_phonenumber` method.

## [0.3.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.3.2) - 2019-06-11
-   Added support to key-list as key.
-   Fixed `setup.py` requirements installation on Python 2.7.

## [0.3.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.3.1) - 2019-06-11
-   Added `dump` and `dump_items` utility methods.

## [0.3.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.3.0) - 2019-06-10
-   Added casting to `benedict` to all dicts returned by any public method.
-   Renamed `get_keypaths` to `keypaths` according to keys and values existing methods.
-   Reorganized lib structure to improve scalability.
-   Added python 2.7 support.
-   Improved code quality.

## [0.2.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.2.0) - 2019-05-20
-   Improved `parse_bool` method.
-   Added keypath support to `pop` method and refactored core methods.
-   Added `get_keypaths` method.
-   Added keypath support to `fromkeys` method.
-   Added `deepcopy` shortcut method.
-   Added keypath support to `copy` method.
-   Refactored `KeypathDict` core methods.

## [0.1.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.1.0) - 2018-05-17
-   Released package on pypi.