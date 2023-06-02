# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.30.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.30.2) - 2023-06-02
-   Allow `ini` format to support nested structures (encode to json only dicts). #284
-   Prevent clearing dict instance when assigning value to itself. #294

## [0.30.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.30.1) - 2023-05-16
-   Allow `ini` format to support nested structures. #284 (#289)
-   Switch from `setup.cfg` to `pyproject.toml`.
-   Replace `flake8` with `Ruff`.
-   Fix `tox` test command.
-   Bump requirements.

## [0.30.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.30.0) - 2023-03-22
-   Add `keyattr_dynamic` property (`False` by default). #261 (#266)
-   Make `ini` serializer case-sensitive by default and accept `optionxform` option. #263 (#265)
-   Fix `TypeError` when decoding `.xls` with `None` columns.
-   Improve decoding errors traceback.
-   Bump requirements.

## [0.29.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.29.1) - 2023-03-09
-   Fix missing dependency on `pyyaml`. #260
-   Fix protected keys in `json` items preventing automatic keys creation when getting `__protected__` attributes. #259

## [0.29.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.29.0) - 2023-03-09
-   `NEW` Add `keyattr` *(keys as attributes)* support. (#257)
-   `NEW` Separate installation targets (extras requires). #200 (#258)
-   Fix set state when loading from pickle.
-   Improve tests coverage.
-   Upgrade syntax for `Python >= 3.8`.
-   Reformat and cleanup code.
-   Move `flake8` config to `setup.cfg`.
-   Increase `flake8` checks.
-   Add `flake8-bugbear` to `pre-commit`.
-   Run `flake8` also on tests files.
-   Run `pre-commit` also with `tox`.
-   Rename default branch from `master` to `main`.
-   Bump requirements.

## [0.28.3](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.28.3) - 2023-01-12
-   Remove `tests/` from dist.
-   Bump requirements.

## [0.28.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.28.2) - 2023-01-11
-   Fix `FileNotFoundError` if file is just the filename. #226
-   Bump requirements.

## [0.28.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.28.1) - 2023-01-02
-   Add `pyupgrade` to `pre-commit` config.
-   Add `setup.cfg` (`setuptools` declarative syntax) generated using `setuptools-py2cfg`.
-   Add support for `pathlib.Path`. #144
-   Bump requirements.

## [0.28.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.28.0) - 2022-12-29
-   Drop `Python 3.7 support`.
-   Replace `str.format` with `f-strings`.
-   Remove `python setup.py test` usage.
-   Remove encoding pragma.
-   Fix `s3_options` option forwarded to `json` decoder. #198 (#204)
-   Bump requirements.

## [0.27.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.27.1) - 2022-11-26
-   Add `Python 3.11` support. #143
-   Add `pre-commit` with `black`, `isort` and `flake8`.
-   Read `toml` files using the standard `tomlib` (if available). #143
-   Bump requirements (`boto3`, `python-slugify`, `orjson`) version.

## [0.27.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.27.0) - 2022-10-12
-   Add `s3` support to I/O operations. #17 (#126)
-   Fix subclasses type. #115 (#124)

## [0.26.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.26.0) - 2022-10-09
-   Add `xls` files (`.xlsx`, `.xlsm`, `.xls`) support (read-only). #70 (#122)
-   Drop `Python 3.6` support. (#123)

## [0.25.4](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.25.4) - 2022-09-06
-   Fix `toml` encoding circular reference error. #110

## [0.25.3](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.25.3) - 2022-08-23
-   Fix set dict item value in list. #109

## [0.25.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.25.2) - 2022-07-15
-   Fixed `orjson` compatibility. #102
-   Fixed `swap` between dict items.
-   Fixed `deepcopy` with pointer.
-   Bumped requirements.

## [0.25.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.25.1) - 2022-04-27
-   Fixed broken `yaml` serialization with `benedict` attributes. #89
-   Fixed `flatten` not working when separator is equal to `keypath_separator`. #88
-   Bumped requirements.

## [0.25.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.25.0) - 2022-02-18
-   Added official `python 3.10` support.
-   Dropped `python 2.7` and `python 3.5` support.
-   Pinned requirements versions.
-   Reformatted code with **Black**.

## [0.24.3](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.24.3) - 2021-10-04
-   Added tuple index support when getting items. #66
-   Added `type_util.is_dict_or_list_or_tuple` method.
-   Improved tests.

## [0.24.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.24.2) - 2021-08-11
-   Fixed `json.dumps()` when `benedict` is initialized with an empty dict. #57 #61
-   Fixed `merge` not working with an empty dict. #59

## [0.24.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.24.1) - 2021-08-01
-   Fixed `json.dumps()` when `benedict` is initialized with an empty dict. #57

## [0.24.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.24.0) - 2021-05-04
-   Added `ini` format support. #36 #40
-   Added `python 3.9` to CI (tox, travis and GitHub actions).
-   Fixed `to_toml` circular reference error. #53
-   Updated `ftfy` requirement version depending on `python` version.
-   Updated (improved) `QueryStringSerializer` regex.

## [0.23.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.23.2) - 2021-01-19
-   Fixed `merge` method lists concat when merging nested dicts. #48
-   Fixed `BaseDict` initialized with `BaseDict` subclass argument.

## [0.23.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.23.1) - 2021-01-14
-   Fixed `get_int_list` with single value.

## [0.23.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.23.0) - 2020-12-24
-   Added `get_date` and `get_date_list` methods.
-   Added `python-fsutil` library for file-system operations.

## [0.22.4](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.22.4) - 2020-12-22
-   Removed `sort_keys=True` by default in `JSON` serializer.

## [0.22.3](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.22.3) - 2020-12-22
-   Added `concat` option to merge method. #45
-   Added `sort_keys=True` by default in `JSON` serializer.
-   Added `memo` option to clone core method.
-   Fixed broken `json.dumps` using cloned instance. #46

## [0.22.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.22.2) - 2020-11-30
-   Fixed `benedict` `yaml` representer. #43

## [0.22.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.22.1) - 2020-11-27
-   Fixed dump `benedict` object to `yaml` not working correctly. #43

## [0.22.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.22.0) - 2020-10-15
-   Added `get_uuid` and `get_uuid_list` methods.

## [0.21.1](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.21.1) - 2020-09-30
-   Fixed performance issue. #39
-   Fixed `to_json` returns empty dict from generator. #38
-   Refactored `BaseDict` class and enforced tests.

## [0.21.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.21.0) - 2020-09-22
-   Added `match` utility method. #11 #16
-   Added `indexes` option support to keypaths method. #13
-   Updated `keypaths` method to use the default `keypath_separator` (`.`) instead of `None`.
-   Fixed `keypath_separator` inheritance when init from another `benedict` instance. #35
-   Fixed `json.dumps` no longer works directly with `benedict`. #34

## [0.20.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.20.0) - 2020-09-20
-   Added `BaseDict` as base class to keep pointer to the initial input dict. #32
-   Added automatic `benedict` casting to all methods that return dict instances.
-   Updated `flatten` method, now a `KeyError` is raised in case of existing key.

## [0.19.0](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.19.0) - 2020-09-11
-   Added `plist` format support.
-   Enforced `IODict` initial check when using filepath or data-string.
-   Improved `KeyError` messages. PR #28
-   Added encoding optional argument to `io_util.read_file` and `io_util.write_file`.
-   Fixed python 3.5/3.6 I/O encoding issue.

## [0.18.2](https://github.com/fabiocaccamo/python-benedict/releases/tag/0.18.2) - 2020-09-02
-   Added `find` method. #23
-   Added `overwrite` option support to merge method. #24
-   Fixed format auto-detection with unexpected extensions. #19

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
