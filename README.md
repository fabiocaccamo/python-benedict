[![](https://img.shields.io/pypi/pyversions/python-benedict.svg?color=blue&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/v/python-benedict.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/python-benedict/)
[![](https://static.pepy.tech/badge/python-benedict/month)](https://pepy.tech/project/python-benedict)
[![](https://img.shields.io/github/stars/fabiocaccamo/python-benedict?logo=github)](https://github.com/fabiocaccamo/python-benedict/stargazers)
[![](https://img.shields.io/pypi/l/python-benedict.svg?color=blue)](https://github.com/fabiocaccamo/python-benedict/blob/main/LICENSE.txt)

[![](https://results.pre-commit.ci/badge/github/fabiocaccamo/python-benedict/main.svg)](https://results.pre-commit.ci/latest/github/fabiocaccamo/python-benedict/main)
[![](https://img.shields.io/github/actions/workflow/status/fabiocaccamo/python-benedict/test-package.yml?branch=main&label=build&logo=github)](https://github.com/fabiocaccamo/python-benedict)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/python-benedict?logo=codecov)](https://codecov.io/gh/fabiocaccamo/python-benedict)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/python-benedict?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/python-benedict/)
[![](https://img.shields.io/codacy/grade/0dbd5cc2089f4dce80a0e49e6822be3c?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/python-benedict)
[![](https://img.shields.io/scrutinizer/quality/g/fabiocaccamo/python-benedict?logo=scrutinizer)](https://scrutinizer-ci.com/g/fabiocaccamo/python-benedict/?branch=main)
[![](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)
[![](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# python-benedict
python-benedict is a dict subclass with **keylist/keypath/keyattr** support, **I/O** shortcuts (`base64`, `cli`, `csv`, `ini`, `json`, `pickle`, `plist`, `query-string`, `toml`, `xls`, `xml`, `yaml`) and many **utilities**... for humans, obviously.

## Features
-   100% **backward-compatible**, you can safely wrap existing dictionaries.
-   `NEW` **Keyattr** support for get/set items using **keys as attributes**.
-   **Keylist** support using **list of keys** as key.
-   **Keypath** support using **keypath-separator** *(dot syntax by default)*.
-   Keypath **list-index** support  *(also negative)* using the standard `[n]` suffix.
-   Normalized **I/O operations** with most common formats: `base64`, `cli`, `csv`, `ini`, `json`, `pickle`, `plist`, `query-string`, `toml`, `xls`, `xml`, `yaml`.
-   Multiple **I/O operations** backends: `file-system` *(read/write)*, `url` *(read-only)*, `s3` *(read/write)*.
-   Many **utility** and **parse methods** to retrieve data as needed *(check the [API](#api) section)*.
-   Well **tested**. ;)

## Index
-   [Installation](#installation)
    -   [Optional Requirements](#optional-requirements)
-   [Usage](#usage)
    -   [Basics](#basics)
    -   [Keyattr](#keyattr) `my_dict.x.y.z`
    -   [Keylist](#keylist) `my_dict["x", "y", "z"]`
    -   [Keypath](#keypath) `my_dict["x.y.z"]`
        -   [Custom keypath separator](#custom-keypath-separator)
        -   [Change keypath separator](#change-keypath-separator)
        -   [Disable keypath functionality](#disable-keypath-functionality)
        -   [List index support](#list-index-support)
    -   [I/O](#io)
    -   [API](#api)
        -   [Utility methods](#utility-methods)
        -   [I/O methods](#io-methods)
        -   [Parse methods](#parse-methods)
-   [Testing](#testing)
-   [License](#license)

## Installation
If you want to install **everything**:
-   Run `pip install "python-benedict[all]"`

alternatively you can install the main package:
-   Run `pip install python-benedict`, then install only the [optional requirements](#optional-requirements) you need.

### Optional Requirements
Here the hierarchy of possible installation targets available when running `pip install "python-benedict[...]"` *(each target installs all its sub-targets)*:
- `[all]`
    - `[io]`
        - `[toml]`
        - `[xls]`
        - `[xml]`
        - `[yaml]`
    - `[parse]`
    - `[s3]`

## Usage

### Basics
`benedict` is a `dict` subclass, so it is possible to use it as a normal dictionary *(you can just cast an existing dict)*.

```python
from benedict import benedict

# create a new empty instance
d = benedict()

# or cast an existing dict
d = benedict(existing_dict)

# or create from data source (filepath, url or data-string) in a supported format:
# Base64, CSV, JSON, TOML, XML, YAML, query-string
d = benedict("https://localhost:8000/data.json", format="json")

# or in a Django view
params = benedict(request.GET.items())
page = params.get_int("page", 1)
```

### Keyattr
It is possible to get/set items using **keys as attributes** (dotted notation).

```python
d = benedict(keyattr_dynamic=True) # default False
d.profile.firstname = "Fabio"
d.profile.lastname = "Caccamo"
print(d) # -> { "profile":{ "firstname":"Fabio", "lastname":"Caccamo" } }
```

By default, if the `keyattr_dynamic` is not explicitly set to `True`, this functionality works for get/set only already existing items.

#### Disable keyattr functionality
You can disable the keyattr functionality passing `keyattr_enabled=False` option in the constructor.

```python
d = benedict(existing_dict, keyattr_enabled=False) # default True
```

or using the `getter/setter` property.

```python
d.keyattr_enabled = False
```

#### Dynamic keyattr functionality
You can enable the dynamic attributes access functionality passing `keyattr_dynamic=True` in the constructor.

```python
d = benedict(existing_dict, keyattr_dynamic=True) # default False
```

or using the `getter/setter` property.

```python
d.keyattr_dynamic = True
```

> **Warning** - even if this feature is very useful, it has some obvious limitations: it works only for string keys that are *unprotected* (not starting with an `_`) and that don't clash with the currently supported methods names.

### Keylist
Wherever a **key** is used, it is possible to use also a **list (or a tuple) of keys**.

```python
d = benedict()

# set values by keys list
d["profile", "firstname"] = "Fabio"
d["profile", "lastname"] = "Caccamo"
print(d) # -> { "profile":{ "firstname":"Fabio", "lastname":"Caccamo" } }
print(d["profile"]) # -> { "firstname":"Fabio", "lastname":"Caccamo" }

# check if keypath exists in dict
print(["profile", "lastname"] in d) # -> True

# delete value by keys list
del d["profile", "lastname"]
print(d["profile"]) # -> { "firstname":"Fabio" }
```

### Keypath
`.` is the default keypath separator.

If you cast an existing dict and its keys contain the keypath separator a `ValueError` will be raised.

In this case you should use a [custom keypath separator](#custom-keypath-separator) or [disable keypath functionality](#disable-keypath-functionality).

```python
d = benedict()

# set values by keypath
d["profile.firstname"] = "Fabio"
d["profile.lastname"] = "Caccamo"
print(d) # -> { "profile":{ "firstname":"Fabio", "lastname":"Caccamo" } }
print(d["profile"]) # -> { "firstname":"Fabio", "lastname":"Caccamo" }

# check if keypath exists in dict
print("profile.lastname" in d) # -> True

# delete value by keypath
del d["profile.lastname"]
```

#### Custom keypath separator
You can customize the keypath separator passing the `keypath_separator` argument in the constructor.

If you pass an existing dict to the constructor and its keys contain the keypath separator an `Exception` will be raised.

```python
d = benedict(existing_dict, keypath_separator="/")
```

#### Change keypath separator
You can change the `keypath_separator` at any time using the `getter/setter` property.

If any existing key contains the new `keypath_separator` an `Exception` will be raised.

```python
d.keypath_separator = "/"
```

#### Disable keypath functionality
You can disable the keypath functionality passing `keypath_separator=None` option in the constructor.

```python
d = benedict(existing_dict, keypath_separator=None)
```

or using the `getter/setter` property.

```python
d.keypath_separator = None
```

#### List index support
List index are supported, keypaths can include indexes *(also negative)* using `[n]`, to perform any operation very fast:

```python
# Eg. get last location cordinates of the first result:
loc = d["results[0].locations[-1].coordinates"]
lat = loc.get_decimal("latitude")
lng = loc.get_decimal("longitude")
```

### I/O

For simplifying I/O operations, `benedict` supports a variety of input/output methods with most common formats: `base64`, `cli`, `csv`, `ini`, `json`, `pickle`, `plist`, `query-string`, `toml`, `xls`, `xml`, `yaml`.

#### Input via constructor

It is possible to create a `benedict` instance directly from data-source (`filepath`, `url`, `s3` or `data-string`) by passing the data source and the data format (optional, default "json") in the constructor.

```python
# filepath
d = benedict("/root/data.yml", format="yaml")

# url
d = benedict("https://localhost:8000/data.xml", format="xml")

# s3
d = benedict("s3://my-bucket/data.xml", s3_options={"aws_access_key_id": "...", "aws_secret_access_key": "..."})

# data-string
d = benedict('{"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9}')
```

#### Input methods

- All *input* methods can be accessed as class methods and are prefixed by `from_*` followed by the format name.
- In all *input* methods, the first argument can represent: **url**, **filepath** or **data-string**.

#### Output methods

- All *output* methods can be accessed as instance methods and are prefixed by `to_*` followed by the format name.
- In all *output* methods, if `filepath="..."` kwarg is specified, the output will be also **saved** at the specified filepath.

#### Supported formats

Here are the details of the supported formats, operations and extra options docs.

| **format**     | **input**          | **output**         | **extra options docs**                                                                |
|----------------|--------------------|--------------------|---------------------------------------------------------------------------------------|
| `base64`       | :white_check_mark: | :white_check_mark: | -                                                                                     |
| `cli`          | :white_check_mark: | :x:                | [argparse](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser)   |
| `csv`          | :white_check_mark: | :white_check_mark: | [csv](https://docs.python.org/3/library/csv.html)                                     |
| `ini`          | :white_check_mark: | :white_check_mark: | [configparser](https://docs.python.org/3/library/configparser.html)                   |
| `json`         | :white_check_mark: | :white_check_mark: | [json](https://docs.python.org/3/library/json.html)                                   |
| `pickle`       | :white_check_mark: | :white_check_mark: | [pickle](https://docs.python.org/3/library/pickle.html)                               |
| `plist`        | :white_check_mark: | :white_check_mark: | [plistlib](https://docs.python.org/3/library/plistlib.html)                           |
| `query-string` | :white_check_mark: | :white_check_mark: | -                                                                                     |
| `toml`         | :white_check_mark: | :white_check_mark: | [toml](https://pypi.org/project/toml/)                                                |
| `xls`          | :white_check_mark: | :x:                | [openpyxl](https://openpyxl.readthedocs.io/) - [xlrd](https://pypi.org/project/xlrd/) |
| `xml`          | :white_check_mark: | :white_check_mark: | [xmltodict](https://github.com/martinblech/xmltodict)                                 |
| `yaml`         | :white_check_mark: | :white_check_mark: | [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation)                                 |

### API

-   **Utility methods**

    -   [`clean`](#clean)
    -   [`clone`](#clone)
    -   [`dump`](#dump)
    -   [`filter`](#filter)
    -   [`find`](#find)
    -   [`flatten`](#flatten)
    -   [`groupby`](#groupby)
    -   [`invert`](#invert)
    -   [`items_sorted_by_keys`](#items_sorted_by_keys)
    -   [`items_sorted_by_values`](#items_sorted_by_values)
    -   [`keypaths`](#keypaths)
    -   [`match`](#match)
    -   [`merge`](#merge)
    -   [`move`](#move)
    -   [`nest`](#nest)
    -   [`remove`](#remove)
    -   [`rename`](#rename)
    -   [`search`](#search)
    -   [`standardize`](#standardize)
    -   [`subset`](#subset)
    -   [`swap`](#swap)
    -   [`traverse`](#traverse)
    -   [`unflatten`](#unflatten)
    -   [`unique`](#unique)

-   **I/O methods**

    -   [`from_base64`](#from_base64)
    -   [`from_cli`](#from_cli)
    -   [`from_csv`](#from_csv)
    -   [`from_ini`](#from_ini)
    -   [`from_json`](#from_json)
    -   [`from_pickle`](#from_pickle)
    -   [`from_plist`](#from_plist)
    -   [`from_query_string`](#from_query_string)
    -   [`from_toml`](#from_toml)
    -   [`from_xls`](#from_xls)
    -   [`from_xml`](#from_xml)
    -   [`from_yaml`](#from_yaml)
    -   [`to_base64`](#to_base64)
    -   [`to_csv`](#to_csv)
    -   [`to_ini`](#to_ini)
    -   [`to_json`](#to_json)
    -   [`to_pickle`](#to_pickle)
    -   [`to_plist`](#to_plist)
    -   [`to_query_string`](#to_query_string)
    -   [`to_toml`](#to_toml)
    -   [`to_xml`](#to_xml)
    -   [`to_yaml`](#to_yaml)

-   **Parse methods**

    -   [`get_bool`](#get_bool)
    -   [`get_bool_list`](#get_bool_list)
    -   [`get_date`](#get_date)
    -   [`get_date_list`](#get_date_list)
    -   [`get_datetime`](#get_datetime)
    -   [`get_datetime_list`](#get_datetime_list)
    -   [`get_decimal`](#get_decimal)
    -   [`get_decimal_list`](#get_decimal_list)
    -   [`get_dict`](#get_dict)
    -   [`get_email`](#get_email)
    -   [`get_float`](#get_float)
    -   [`get_float_list`](#get_float_list)
    -   [`get_int`](#get_int)
    -   [`get_int_list`](#get_int_list)
    -   [`get_list`](#get_list)
    -   [`get_list_item`](#get_list_item)
    -   [`get_phonenumber`](#get_phonenumber)
    -   [`get_slug`](#get_slug)
    -   [`get_slug_list`](#get_slug_list)
    -   [`get_str`](#get_str)
    -   [`get_str_list`](#get_str_list)
    -   [`get_uuid`](#get_uuid)
    -   [`get_uuid_list`](#get_uuid_list)

### Utility methods

These methods are common utilities that will speed up your everyday work.

Utilities that accept key argument(s) also support keypath(s).

Utilities that return a dictionary always return a new `benedict` instance.

#### `clean`

```python
# Clean the current dict instance removing all empty values: None, "", {}, [], ().
# If strings or collections (dict, list, set, tuple) flags are False,
# related empty values will not be deleted.
d.clean(strings=True, collections=True)
```

#### `clone`

```python
# Return a clone (deepcopy) of the dict.
c = d.clone()
```

#### `dump`

```python
# Return a readable representation of any dict/list.
# This method can be used both as static method or instance method.
s = benedict.dump(d.keypaths())
print(s)
# or
d = benedict()
print(d.dump())
```

#### `filter`

```python
# Return a filtered dict using the given predicate function.
# Predicate function receives key, value arguments and should return a bool value.
predicate = lambda k, v: v is not None
f = d.filter(predicate)
```

#### `find`

```python
# Return the first match searching for the given keys/keypaths.
# If no result found, default value is returned.
keys = ["a.b.c", "m.n.o", "x.y.z"]
f = d.find(keys, default=0)
```

#### `flatten`

```python
# Return a new flattened dict using the given separator to join nested dict keys to flatten keypaths.
f = d.flatten(separator="_")
```

#### `groupby`

```python
# Group a list of dicts at key by the value of the given by_key and return a new dict.
g = d.groupby("cities", by_key="country_code")
```

#### `invert`

```python
# Return an inverted dict where values become keys and keys become values.
# Since multiple keys could have the same value, each value will be a list of keys.
# If flat is True each value will be a single value (use this only if values are unique).
i = d.invert(flat=False)
```

#### `items_sorted_by_keys`

```python
# Return items (key/value list) sorted by keys.
# If reverse is True, the list will be reversed.
items = d.items_sorted_by_keys(reverse=False)
```

#### `items_sorted_by_values`

```python
# Return items (key/value list) sorted by values.
# If reverse is True, the list will be reversed.
items = d.items_sorted_by_values(reverse=False)
```

#### `keypaths`

```python
# Return a list of all keypaths in the dict.
# If indexes is True, the output will include list values indexes.
k = d.keypaths(indexes=False)
```

#### `match`

```python
# Return a list of all values whose keypath matches the given pattern (a regex or string).
# If pattern is string, wildcard can be used (eg. [*] can be used to match all list indexes).
# If indexes is True, the pattern will be matched also against list values.
m = d.match(pattern, indexes=True)
```

#### `merge`

```python
# Merge one or more dictionary objects into current instance (deepupdate).
# Sub-dictionaries keys will be merged together.
# If overwrite is False, existing values will not be overwritten.
# If concat is True, list values will be concatenated together.
d.merge(a, b, c, overwrite=True, concat=False)
```

#### `move`

```python
# Move an item from key_src to key_dst.
# It can be used to rename a key.
# If key_dst exists, its value will be overwritten.
d.move("a", "b", overwrite=True)
```

#### `nest`

```python
# Nest a list of dicts at the given key and return a new nested list
# using the specified keys to establish the correct items hierarchy.
d.nest("values", id_key="id", parent_id_key="parent_id", children_key="children")
```

#### `remove`

```python
# Remove multiple keys from the dict.
# It is possible to pass a single key or more keys (as list or *args).
d.remove(["firstname", "lastname", "email"])
```

#### `rename`

```python
# Rename a dict item key from "key" to "key_new".
# If key_new exists, a KeyError will be raised.
d.rename("first_name", "firstname")
```

#### `search`

```python
# Search and return a list of items (dict, key, value, ) matching the given query.
r = d.search("hello", in_keys=True, in_values=True, exact=False, case_sensitive=False)
```

#### `standardize`

```python
# Standardize all dict keys, e.g. "Location Latitude" -> "location_latitude".
d.standardize()
```

#### `subset`

```python
# Return a dict subset for the given keys.
# It is possible to pass a single key or more keys (as list or *args).
s = d.subset(["firstname", "lastname", "email"])
```

#### `swap`

```python
# Swap items values at the given keys.
d.swap("firstname", "lastname")
```

#### `traverse`

```python
# Traverse a dict passing each item (dict, key, value) to the given callback function.
def f(d, key, value):
    print(f"dict: {d} - key: {key} - value: {value}")
d.traverse(f)
```

#### `unflatten`

```python
# Return a new unflattened dict using the given separator to split dict keys to nested keypaths.
u = d.unflatten(separator="_")
```

#### `unique`

```python
# Remove duplicated values from the dict.
d.unique()
```

### I/O methods

These methods are available for input/output operations.

#### `from_base64`

```python
# Try to load/decode a base64 encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to choose the subformat used under the hood:
# ('csv', 'json', 'query-string', 'toml', 'xml', 'yaml'), default: 'json'.
# It's possible to choose the encoding, default 'utf-8'.
# A ValueError is raised in case of failure.
d = benedict.from_base64(s, subformat="json", encoding="utf-8", **kwargs)
```

#### `from_cli`

```python
# Load and decode data from a string of CLI arguments.
# ArgumentParser specific options can be passed using kwargs:
# https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
# Return a new dict instance. A ValueError is raised in case of failure.
d = benedict.from_cli(s, **kwargs)
```

#### `from_csv`

```python
# Try to load/decode a csv encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to specify the columns list, default: None (in this case the first row values will be used as keys).
# It's possible to pass decoder specific options using kwargs:
# https://docs.python.org/3/library/csv.html
# A ValueError is raised in case of failure.
d = benedict.from_csv(s, columns=None, columns_row=True, **kwargs)
```

#### `from_ini`

```python
# Try to load/decode a ini encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://docs.python.org/3/library/configparser.html
# A ValueError is raised in case of failure.
d = benedict.from_ini(s, **kwargs)
```

#### `from_json`

```python
# Try to load/decode a json encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://docs.python.org/3/library/json.html
# A ValueError is raised in case of failure.
d = benedict.from_json(s, **kwargs)
```

#### `from_pickle`

```python
# Try to load/decode a pickle encoded in Base64 format and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://docs.python.org/3/library/pickle.html
# A ValueError is raised in case of failure.
d = benedict.from_pickle(s, **kwargs)
```

#### `from_plist`

```python
# Try to load/decode a p-list encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://docs.python.org/3/library/plistlib.html
# A ValueError is raised in case of failure.
d = benedict.from_plist(s, **kwargs)
```

#### `from_query_string`

```python
# Try to load/decode a query-string and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# A ValueError is raised in case of failure.
d = benedict.from_query_string(s, **kwargs)
```

#### `from_toml`

```python
# Try to load/decode a toml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://pypi.org/project/toml/
# A ValueError is raised in case of failure.
d = benedict.from_toml(s, **kwargs)
```

#### `from_xls`

```python
# Try to load/decode a xls file (".xls", ".xlsx", ".xlsm") from url, filepath or data-string.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# - https://openpyxl.readthedocs.io/ (for .xlsx and .xlsm files)
# - https://pypi.org/project/xlrd/ (for .xls files)
# A ValueError is raised in case of failure.
d = benedict.from_xls(s, sheet=0, columns=None, columns_row=True, **kwargs)
```

#### `from_xml`

```python
# Try to load/decode a xml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://github.com/martinblech/xmltodict
# A ValueError is raised in case of failure.
d = benedict.from_xml(s, **kwargs)
```

#### `from_yaml`

```python
# Try to load/decode a yaml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs:
# https://pyyaml.org/wiki/PyYAMLDocumentation
# A ValueError is raised in case of failure.
d = benedict.from_yaml(s, **kwargs)
```

#### `to_base64`

```python
# Return the dict instance encoded in base64 format and optionally save it at the specified 'filepath'.
# It's possible to choose the subformat used under the hood:
# ('csv', json', 'query-string', 'toml', 'xml', 'yaml'), default: 'json'.
# It's possible to choose the encoding, default 'utf-8'.
# It's possible to pass decoder specific options using kwargs.
# A ValueError is raised in case of failure.
s = d.to_base64(subformat="json", encoding="utf-8", **kwargs)
```

#### `to_csv`

```python
# Return a list of dicts in the current dict encoded in csv format and optionally save it at the specified filepath.
# It's possible to specify the key of the item (list of dicts) to encode, default: 'values'.
# It's possible to specify the columns list, default: None (in this case the keys of the first item will be used).
# A ValueError is raised in case of failure.
s = d.to_csv(key="values", columns=None, columns_row=True, **kwargs)
```

#### `to_ini`

```python
# Return the dict instance encoded in ini format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs:
# https://docs.python.org/3/library/configparser.html
# A ValueError is raised in case of failure.
s = d.to_ini(**kwargs)
```

#### `to_json`

```python
# Return the dict instance encoded in json format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs:
# https://docs.python.org/3/library/json.html
# A ValueError is raised in case of failure.
s = d.to_json(**kwargs)
```

#### `to_pickle`

```python
# Return the dict instance as pickle encoded in Base64 format and optionally save it at the specified filepath.
# The pickle protocol used by default is 2.
# It's possible to pass encoder specific options using kwargs:
# https://docs.python.org/3/library/pickle.html
# A ValueError is raised in case of failure.
s = d.to_pickle(**kwargs)
```

#### `to_plist`

```python
# Return the dict instance encoded in p-list format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs:
# https://docs.python.org/3/library/plistlib.html
# A ValueError is raised in case of failure.
s = d.to_plist(**kwargs)
```

#### `to_query_string`

```python
# Return the dict instance as query-string and optionally save it at the specified filepath.
# A ValueError is raised in case of failure.
s = d.to_query_string(**kwargs)
```

#### `to_toml`

```python
# Return the dict instance encoded in toml format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs:
# https://pypi.org/project/toml/
# A ValueError is raised in case of failure.
s = d.to_toml(**kwargs)
```

#### `to_xml`

```python
# Return the dict instance encoded in xml format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs:
# https://github.com/martinblech/xmltodict
# A ValueError is raised in case of failure.
s = d.to_xml(**kwargs)
```

#### `to_yaml`

```python
# Return the dict instance encoded in yaml format.
# If filepath option is passed the output will be saved ath
# It's possible to pass encoder specific options using kwargs:
# https://pyyaml.org/wiki/PyYAMLDocumentation
# A ValueError is raised in case of failure.
s = d.to_yaml(**kwargs)
```

### Parse methods

These methods are wrappers of the `get` method, they parse data trying to return it in the expected type.

#### `get_bool`

```python
# Get value by key or keypath trying to return it as bool.
# Values like `1`, `true`, `yes`, `on`, `ok` will be returned as `True`.
d.get_bool(key, default=False)
```

#### `get_bool_list`

```python
# Get value by key or keypath trying to return it as list of bool values.
# If separator is specified and value is a string it will be splitted.
d.get_bool_list(key, default=[], separator=",")
```

#### `get_date`

```python
# Get value by key or keypath trying to return it as date.
# If format is not specified it will be autodetected.
# If choices and value is in choices return value otherwise default.
d.get_date(key, default=None, format=None, choices=[])
```

#### `get_date_list`

```python
# Get value by key or keypath trying to return it as list of date values.
# If separator is specified and value is a string it will be splitted.
d.get_date_list(key, default=[], format=None, separator=",")
```

#### `get_datetime`

```python
# Get value by key or keypath trying to return it as datetime.
# If format is not specified it will be autodetected.
# If choices and value is in choices return value otherwise default.
d.get_datetime(key, default=None, format=None, choices=[])
```

#### `get_datetime_list`

```python
# Get value by key or keypath trying to return it as list of datetime values.
# If separator is specified and value is a string it will be splitted.
d.get_datetime_list(key, default=[], format=None, separator=",")
```

#### `get_decimal`

```python
# Get value by key or keypath trying to return it as Decimal.
# If choices and value is in choices return value otherwise default.
d.get_decimal(key, default=Decimal("0.0"), choices=[])
```

#### `get_decimal_list`

```python
# Get value by key or keypath trying to return it as list of Decimal values.
# If separator is specified and value is a string it will be splitted.
d.get_decimal_list(key, default=[], separator=",")
```

#### `get_dict`

```python
# Get value by key or keypath trying to return it as dict.
# If value is a json string it will be automatically decoded.
d.get_dict(key, default={})
```

#### `get_email`

```python
# Get email by key or keypath and return it.
# If value is blacklisted it will be automatically ignored.
# If check_blacklist is False, it will be not ignored even if blacklisted.
d.get_email(key, default="", choices=None, check_blacklist=True)
```

#### `get_float`

```python
# Get value by key or keypath trying to return it as float.
# If choices and value is in choices return value otherwise default.
d.get_float(key, default=0.0, choices=[])
```

#### `get_float_list`

```python
# Get value by key or keypath trying to return it as list of float values.
# If separator is specified and value is a string it will be splitted.
d.get_float_list(key, default=[], separator=",")
```

#### `get_int`

```python
# Get value by key or keypath trying to return it as int.
# If choices and value is in choices return value otherwise default.
d.get_int(key, default=0, choices=[])
```

#### `get_int_list`

```python
# Get value by key or keypath trying to return it as list of int values.
# If separator is specified and value is a string it will be splitted.
d.get_int_list(key, default=[], separator=",")
```

#### `get_list`

```python
# Get value by key or keypath trying to return it as list.
# If separator is specified and value is a string it will be splitted.
d.get_list(key, default=[], separator=",")
```

#### `get_list_item`

```python
# Get list by key or keypath and return value at the specified index.
# If separator is specified and list value is a string it will be splitted.
d.get_list_item(key, index=0, default=None, separator=",")
```

#### `get_phonenumber`

```python
# Get phone number by key or keypath and return a dict with different formats (e164, international, national).
# If country code is specified (alpha 2 code), it will be used to parse phone number correctly.
d.get_phonenumber(key, country_code=None, default=None)
```

#### `get_slug`

```python
# Get value by key or keypath trying to return it as slug.
# If choices and value is in choices return value otherwise default.
d.get_slug(key, default="", choices=[])
```

#### `get_slug_list`

```python
# Get value by key or keypath trying to return it as list of slug values.
# If separator is specified and value is a string it will be splitted.
d.get_slug_list(key, default=[], separator=",")
```

#### `get_str`

```python
# Get value by key or keypath trying to return it as string.
# Encoding issues will be automatically fixed.
# If choices and value is in choices return value otherwise default.
d.get_str(key, default="", choices=[])
```

#### `get_str_list`

```python
# Get value by key or keypath trying to return it as list of str values.
# If separator is specified and value is a string it will be splitted.
d.get_str_list(key, default=[], separator=",")
```

#### `get_uuid`

```python
# Get value by key or keypath trying to return it as valid uuid.
# If choices and value is in choices return value otherwise default.
d.get_uuid(key, default="", choices=[])
```

#### `get_uuid_list`

```python
# Get value by key or keypath trying to return it as list of valid uuid values.
# If separator is specified and value is a string it will be splitted.
d.get_uuid_list(key, default=[], separator=",")
```

## Testing
```bash
# clone repository
git clone https://github.com/fabiocaccamo/python-benedict.git && cd python-benedict

# create virtualenv and activate it
python -m venv venv && . venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip

# install requirements
pip install -r requirements.txt -r requirements-test.txt

# install pre-commit to run formatters and linters
pre-commit install --install-hooks

# run tests using tox
tox

# or run tests using unittest
python -m unittest
```

## License
Released under [MIT License](LICENSE.txt).

---

## Supporting

- :star: Star this project on [GitHub](https://github.com/fabiocaccamo/python-benedict)
- :octocat: Follow me on [GitHub](https://github.com/fabiocaccamo)
- :blue_heart: Follow me on [Twitter](https://twitter.com/fabiocaccamo)
- :moneybag: Sponsor me on [Github](https://github.com/sponsors/fabiocaccamo)

## See also

- [`python-fontbro`](https://github.com/fabiocaccamo/python-fontbro) - friendly font operations. 🧢

- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️
