[![Build Status](https://travis-ci.org/fabiocaccamo/python-benedict.svg?branch=master)](https://travis-ci.org/fabiocaccamo/python-benedict)
[![codecov](https://codecov.io/gh/fabiocaccamo/python-benedict/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/python-benedict)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0dbd5cc2089f4dce80a0e49e6822be3c)](https://www.codacy.com/app/fabiocaccamo/python-benedict)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fabiocaccamo/python-benedict/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fabiocaccamo/python-benedict/?branch=master)
[![Requirements Status](https://requires.io/github/fabiocaccamo/python-benedict/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/python-benedict/requirements/?branch=master)
[![PyPI version](https://badge.fury.io/py/python-benedict.svg)](https://badge.fury.io/py/python-benedict)
[![PyPI downloads](https://img.shields.io/pypi/dm/python-benedict.svg)](https://img.shields.io/pypi/dm/python-benedict.svg)
[![Py versions](https://img.shields.io/pypi/pyversions/python-benedict.svg)](https://img.shields.io/pypi/pyversions/python-benedict.svg)
[![License](https://img.shields.io/pypi/l/python-benedict.svg)](https://img.shields.io/pypi/l/python-benedict.svg)

# python-benedict
python-benedict is a dict subclass with **keypath** support, **I/O** shortcuts (`Base64`, `JSON`, `TOML`, `XML`, `YAML`, `query-string`) and many **utilities**... for humans, obviously.

## Index
-   [Features](#features)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Usage](#usage)
    -   [Basics](#basics)
    -   [Keypath](#keypath)
        -   [Custom keypath separator](#custom-keypath-separator)
        -   [Change keypath separator](#change-keypath-separator)
        -   [Disable keypath functionality](#disable-keypath-functionality)
-   [API](#api)
    -   [Utility](#utility)
        -   [`clean`](#clean)
        -   [`clone`](#clone)
        -   [`dump`](#dump)
        -   [`filter`](#filter)
        -   [`flatten`](#flatten)
        -   [`invert`](#invert)
        -   [`items_sorted_by_keys`](#items_sorted_by_keys)
        -   [`items_sorted_by_values`](#items_sorted_by_values)
        -   [`keypaths`](#keypaths)
        -   [`merge`](#merge)
        -   [`move`](#move)
        -   [`remove`](#remove)
        -   [`standardize`](#standardize)
        -   [`subset`](#subset)
        -   [`swap`](#swap)
        -   [`traverse`](#traverse)
        -   [`unique`](#unique)
    -   [I/O](#io)
        -   [`from_base64`](#from_base64)
        -   [`from_json`](#from_json)
        -   [`from_query_string`](#from_query_string)
        -   [`from_toml`](#from_toml)
        -   [`from_xml`](#from_xml)
        -   [`from_yaml`](#from_yaml)
        -   [`to_base64`](#to_base64)
        -   [`to_json`](#to_json)
        -   [`to_query_string`](#to_query_string)
        -   [`to_toml`](#to_toml)
        -   [`to_xml`](#to_xml)
        -   [`to_yaml`](#to_yaml)
    -   [Parse](#parse)
        -   [`get_bool`](#get_bool)
        -   [`get_bool_list`](#get_bool_list)
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
-   [Testing](#testing)
-   [License](#license)

## Features
-   Full **keypath** support using **keypath-separator** *(dot syntax by default)* or **list of keys**.
-   Easy **I/O operations** with most common formats: `Base64`, `JSON`, `TOML`, `XML`, `YAML`, `query-string`
-   Many **utility** and **parse methods** to retrieve data as needed *(all methods listed below)*
-   Well **tested**, check the badges ;)
-   100% **backward-compatible** *(you can replace existing dicts without pain)*

## Requirements
-   Python 2.7, 3.4, 3.5, 3.6, 3.7

## Installation
-   Run `pip install python-benedict`

## Usage

### Basics
`benedict` is a `dict` subclass, so it is possible to use it as a normal dictionary *(you can just cast an existing dict)*.

```python
from benedict import benedict

# create a new empty instance
d = benedict()

# or cast an existing dict
d = benedict(existing_dict)

# or create from data source (filepath, url or data-string) in a supported format (base64, json, toml, xml, yaml, query-string)
d = benedict('https://localhost:8000/data.json')

# or in a Django view
params = benedict(request.GET.items())
page = params.get_int('p', 0)
```

### Keypath
`.` is the default keypath separator.

If you cast an existing dict and its keys contain the keypath separator a `ValueError` will be raised.

In this case you should use a [custom keypath separator](#custom-keypath-separator) or [disable keypath functionality](#disable-keypath-functionality).

```python
d = benedict()

# set values by keypath
d['profile.firstname'] = 'Fabio'
d['profile.lastname'] = 'Caccamo'
print(d) # -> { 'profile':{ 'firstname':'Fabio', 'lastname':'Caccamo' } }
print(d['profile']) # -> { 'firstname':'Fabio', 'lastname':'Caccamo' }

# check if keypath exists in dict
print('profile.lastname' in d) # -> True

# delete value by keypath
del d['profile.lastname']
```

It is possible to do the same using a **list of keys**:

```python
d = benedict()

# set values by keys list
d['profile', 'firstname'] = 'Fabio'
d['profile', 'lastname'] = 'Caccamo'
print(d) # -> { 'profile':{ 'firstname':'Fabio', 'lastname':'Caccamo' } }
print(d['profile']) # -> { 'firstname':'Fabio', 'lastname':'Caccamo' }

# check if keypath exists in dict
print(['profile', 'lastname'] in d) # -> True

# delete value by keys list
del d['profile', 'lastname']
```

#### Custom keypath separator
You can customize the keypath separator passing the `keypath_separator` argument in the constructor.

If you pass an existing dict to the constructor and its keys contain the keypath separator an `Exception` will be raised.

```python
d = benedict(existing_dict, keypath_separator='/')
```

#### Change keypath separator
You can change the `keypath_separator` at any time using the `getter/setter` property.

If any existing key contains the new `keypath_separator` an `Exception` will be raised.

```python
d.keypath_separator = '/'
```

#### Disable keypath functionality
You can disable the keypath functionality passing `keypath_separator=None` in the constructor.

```python
d = benedict(existing_dict, keypath_separator=None)
```

You can disable the keypath functionality using the `getter/setter` property.

```python
d.keypath_separator = None
```

## API

### Utility
These methods are common utilities that will speed up your everyday work.

Utilities that accepts key argument(s) also accepts keypath(s).

Utilities that return a dictionary always return a new `benedict` instance.

-   #### clean

```python
# Clean the current dict removing all empty values: None, '', {}, [], ().
# If strings, dicts or lists flags are False, related empty values will not be deleted.
d.clean(strings=True, dicts=True, lists=True)
```

-   #### clone

```python
# Return a clone (deepcopy) of the dict.
c = d.clone()
```

-   #### dump

```python
# Return a readable representation of any dict/list.
# This method can be used both as static method or instance method.
s = benedict.dump(d.keypaths())
print(s)
# or
d = benedict()
print(d.dump())
```

-   #### filter

```python
# Return a filtered dict using the given predicate function.
# Predicate function receives key, value arguments and should return a bool value.
predicate = lambda k, v: v is not None
f = d.filter(predicate)
```

-   #### flatten

```python
# Return a flatten dict using the given separator to concat nested dict keys.
f = d.flatten(separator='_')
```

-   #### invert

```python
# Return an inverted dict where values become keys and keys become values.
# Since multiple keys could have the same value, each value will be a list of keys.
# If flat is True each value will be a single value (use this only if values are unique).
i = d.invert(flat=False)
```

-   #### items_sorted_by_keys

```python
# Return items (key/value list) sorted by keys.
# If reverse is True, the list will be reversed.
items = d.items_sorted_by_keys(reverse=False)
```

-   #### items_sorted_by_values

```python
# Return items (key/value list) sorted by values.
# If reverse is True, the list will be reversed.
items = d.items_sorted_by_values(reverse=False)
```

-   #### keypaths

```python
# Return a list of all keypaths in the dict.
k = d.keypaths()
print(k)
```

-   #### merge

```python
# Merge one or more dictionary objects into current instance (deepupdate).
# Sub-dictionaries keys will be merged toghether.
d.merge(a, b, c)
```

-   #### move

```python
# Move an item from key_src to key_dst.
# It can be used to rename a key.
# If key_dst exists, its value will be overwritten.
d.move('a', 'b')
```

-   #### remove

```python
# Remove multiple keys from the dict.
# It is possible to pass a single key or more keys (as list or *args).
d.remove(['firstname', 'lastname', 'email'])
```

-   #### standardize

```python
# Standardize all dict keys, e.g. "Location Latitude" -> "location_latitude".
d.standardize()
```

-   #### subset

```python
# Return a dict subset for the given keys.
# It is possible to pass a single key or more keys (as list or *args).
s = d.subset(['firstname', 'lastname', 'email'])
```

-   #### swap

```python
# Swap items values at the given keys.
d.swap('firstname', 'lastname')
```

-   #### traverse

```python
# Traverse a dict passing each item (dict, key, value) to the given callback function.
def f(d, key, value):
    print('dict: {} - key: {} - value: {}'.format(d, key, value))
d.traverse(f)
```

-   #### unique

```python
# Remove duplicated values from the dict.
d.unique()
```

### I/O

It is possible to create a `benedict` instance directly from data source (filepath, url or data-string) by passing the data source as first argument in the constructor.

```python
# filepath
d = benedict('/root/data.yml')

# url
d = benedict('https://localhost:8000/data.xml')

# data-string
d = benedict('{"a": 1, "b": 2, "c": 3, "x": 7, "y": 8, "z": 9}')
```

These methods simplify I/O operations with most common formats: `base64`, `json`, `toml`, `xml`, `yaml`, `query-string`

-   #### from_base64

```python
# Try to load/decode a base64 encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to choose the format used under the hood ('json', 'toml', 'xml', 'yaml') default 'json'.
# It's possible to pass decoder specific options using kwargs.
# A ValueError is raised in case of failure.
d = benedict.from_base64(s, format='json', **kwargs)
```

-   #### from_json

```python
# Try to load/decode a json encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs: https://docs.python.org/3/library/json.html
# A ValueError is raised in case of failure.
d = benedict.from_json(s, **kwargs)
```

-   #### from_toml

```python
# Try to load/decode a toml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs: https://pypi.org/project/toml/
# A ValueError is raised in case of failure.
d = benedict.from_toml(s, **kwargs)
```

-   #### from_query_string

```python
# Try to load/decode a query-string and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# A ValueError is raised in case of failure.
d = benedict.from_query_string(s, **kwargs)
```

-   #### from_xml

```python
# Try to load/decode a xml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs: https://github.com/martinblech/xmltodict
# A ValueError is raised in case of failure.
d = benedict.from_xml(s, **kwargs)
```

-   #### from_yaml

```python
# Try to load/decode a yaml encoded data and return it as benedict instance.
# Accept as first argument: url, filepath or data-string.
# It's possible to pass decoder specific options using kwargs: https://pyyaml.org/wiki/PyYAMLDocumentation
# A ValueError is raised in case of failure.
d = benedict.from_yaml(s, **kwargs)
```

-   #### to_base64

```python
# Return the dict instance encoded in base64 format and optionally save it at the specified filepath.
# It's possible to choose the format used under the hood ('json', 'toml', 'xml', 'yaml') default 'json'.
# It's possible to pass decoder specific options using kwargs.
# A ValueError is raised in case of failure.
s = d.to_base64(filepath='', format='json', **kwargs)
```

-   #### to_json

```python
# Return the dict instance encoded in json format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs: https://docs.python.org/3/library/json.html
# A ValueError is raised in case of failure.
s = d.to_json(filepath='', **kwargs)
```

-   #### to_query_string

```python
# Return the dict instance as query-string and optionally save it at the specified filepath.
# A ValueError is raised in case of failure.
s = d.to_query_string(filepath='', **kwargs)
```

-   #### to_toml

```python
# Return the dict instance encoded in toml format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs: https://pypi.org/project/toml/
# A ValueError is raised in case of failure.
s = d.to_toml(filepath='', **kwargs)
```

-   #### to_xml

```python
# Return the dict instance encoded in xml format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs: https://github.com/martinblech/xmltodict
# A ValueError is raised in case of failure.
s = d.to_xml(filepath='', **kwargs)
```

-   #### to_yaml

```python
# Return the dict instance encoded in yaml format and optionally save it at the specified filepath.
# It's possible to pass encoder specific options using kwargs: https://pyyaml.org/wiki/PyYAMLDocumentation
# A ValueError is raised in case of failure.
s = d.to_yaml(filepath='', **kwargs)
```

### Parse
These methods are wrappers of the `get` method, they parse data trying to return it in the expected type.

-   #### get_bool

```python
# Get value by key or keypath trying to return it as bool.
# Values like `1`, `true`, `yes`, `on`, `ok` will be returned as `True`.
d.get_bool(key, default=False)
```

-   #### get_bool_list

```python
# Get value by key or keypath trying to return it as list of bool values.
# If separator is specified and value is a string it will be splitted.
d.get_bool_list(key, default=[], separator=',')
```

-   #### get_datetime

```python
# Get value by key or keypath trying to return it as datetime.
# If format is not specified it will be autodetected.
# If options and value is in options return value otherwise default.
d.get_datetime(key, default=None, format=None, options=[])
```

-   #### get_datetime_list

```python
# Get value by key or keypath trying to return it as list of datetime values.
# If separator is specified and value is a string it will be splitted.
d.get_datetime_list(key, default=[], format=None, separator=',')
```

-   #### get_decimal

```python
# Get value by key or keypath trying to return it as Decimal.
# If options and value is in options return value otherwise default.
d.get_decimal(key, default=Decimal('0.0'), options=[])
```

-   #### get_decimal_list

```python
# Get value by key or keypath trying to return it as list of Decimal values.
# If separator is specified and value is a string it will be splitted.
d.get_decimal_list(key, default=[], separator=',')
```

-   #### get_dict

```python
# Get value by key or keypath trying to return it as dict.
# If value is a json string it will be automatically decoded.
d.get_dict(key, default={})
```

-   #### get_email

```python
# Get email by key or keypath and return it.
# If value is blacklisted it will be automatically ignored.
# If check_blacklist is False, it will be not ignored even if blacklisted.
d.get_email(key, default='', options=None, check_blacklist=True)
```

-   #### get_float

```python
# Get value by key or keypath trying to return it as float.
# If options and value is in options return value otherwise default.
d.get_float(key, default=0.0, options=[])
```

-   #### get_float_list

```python
# Get value by key or keypath trying to return it as list of float values.
# If separator is specified and value is a string it will be splitted.
d.get_float_list(key, default=[], separator=',')
```

-   #### get_int

```python
# Get value by key or keypath trying to return it as int.
# If options and value is in options return value otherwise default.
d.get_int(key, default=0, options=[])
```

-   #### get_int_list

```python
# Get value by key or keypath trying to return it as list of int values.
# If separator is specified and value is a string it will be splitted.
d.get_int_list(key, default=[], separator=',')
```

-   #### get_list

```python
# Get value by key or keypath trying to return it as list.
# If separator is specified and value is a string it will be splitted.
d.get_list(key, default=[], separator=',')
```

-   #### get_list_item

```python
# Get list by key or keypath and return value at the specified index.
# If separator is specified and list value is a string it will be splitted.
d.get_list_item(key, index=0, default=None, separator=',')
```

-   #### get_phonenumber

```python
# Get phone number by key or keypath and return a dict with different formats (e164, international, national).
# If country code is specified (alpha 2 code), it will be used to parse phone number correctly.
d.get_phonenumber(key, country_code=None, default=None)
```

-   #### get_slug

```python
# Get value by key or keypath trying to return it as slug.
# If options and value is in options return value otherwise default.
d.get_slug(key, default='', options=[])
```

-   #### get_slug_list

```python
# Get value by key or keypath trying to return it as list of slug values.
# If separator is specified and value is a string it will be splitted.
d.get_slug_list(key, default=[], separator=',')
```

-   #### get_str

```python
# Get value by key or keypath trying to return it as string.
# Encoding issues will be automatically fixed.
# If options and value is in options return value otherwise default.
d.get_str(key, default='', options=[])
```

-   #### get_str_list

```python
# Get value by key or keypath trying to return it as list of str values.
# If separator is specified and value is a string it will be splitted.
d.get_str_list(key, default=[], separator=',')
```

## Testing
-   Run `tox` / `python setup.py test`

## License
Released under [MIT License](LICENSE.txt).