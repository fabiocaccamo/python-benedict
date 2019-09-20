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
The Python dictionary for humans dealing with evil/complex data.

## Index
-   [Features](#features)
-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Usage](#usage)
    -   [Basics](#basics)
    -   [Keypath](#keypath)
        -   [List keypaths](#list-keypaths)
        -   [Custom keypath separator](#custom-keypath-separator)
        -   [Disable keypath functionality](#disable-keypath-functionality)
-   [API](#api)
    -   [I/O](#io)
        -   [`from_json`](#from_json)
        -   [`from_toml`](#from_toml)
        -   [`from_yaml`](#from_yaml)
        -   [`to_json`](#to_json)
        -   [`to_toml`](#to_toml)
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
    -   [Utility](#utility)
        -   [`clean`](#clean)
        -   [`clone`](#clone)
        -   [`dump`](#dump)
        -   [`filter`](#filter)
        -   [`flatten`](#flatten)
        -   [`merge`](#merge)
        -   [`remove`](#remove)
        -   [`subset`](#subset)
-   [Testing](#testing)
-   [License](#license)

## Features
-   Full **keypath** support *(using the dot syntax by default)*
-   Easy **I/O operations** with most common formats: `json`, `toml`, `yaml`
-   Many **utility** and **parse methods** to retrieve data as needed *(all methods listed below)*
-   Give **benediction** :) to `dict` values before they are returned *(they receive benedict casting)*
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

# create a new instance
d = benedict()

# or cast an existing dict
d = benedict(existing_dict)

# or in a Django view
params = benedict(request.GET.items())
page = params.get_int('p', 0)
```

### Keypath
`.` is the default keypath separator.

If you cast an existing dict and its keys contain the keypath separator a `ValueError` will be raised.

In this case you should use a [custom keypath separator](#custom-keypath-separator) or [disable keypath support](#disable-keypath-support).

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

#### List keypaths
You can list all the `keypaths` available in the `dict`:

```python
# return a list of all keypaths in the dict.
k = d.keypaths()
print(k)
```

#### Custom keypath separator
You can customize the keypath separator passing the `keypath_separator` argument in the constructor.

```python
d = benedict(existing_dict, keypath_separator='/')
```

#### Disable keypath functionality
You can disable the keypath functionality passing `keypath_separator=None` in the constructor.

```python
d = benedict(existing_dict, keypath_separator='/')
```

## API

### I/O
These methods simplify I/O operations with most common formats: `json`, `toml`, `yaml`

-   ##### from_json

```python
# Try to load/decode a json encoded string and return it as dict instance.
# Accept as first argument: url, filepath or string.
# A ValueError is raised in case of failure.
benedict.from_json(s)
```

-   ##### from_toml

```python
# Try to load/decode a toml encoded string and return it as dict instance.
# Accept as first argument: url, filepath or string.
# A ValueError is raised in case of failure.
benedict.from_toml(s)
```

-   ##### from_yaml

```python
# Try to load/decode a yaml encoded string and return it as dict instance.
# Accept as first argument: url, filepath or string.
# A ValueError is raised in case of failure.
benedict.from_yaml(s)
```

-   ##### to_json

```python
# Return the dict instance encoded in json format and optionally save it at the specified filepath.
# It's possible to pass custom options to the encoder using kwargs, eg. sort_keys=True.
# A ValueError is raised in case of failure.
s = d.to_json(filepath='', **kwargs)
```

-   ##### to_toml

```python
# Return the dict instance encoded in toml format and optionally save it at the specified filepath.
# It's possible to pass custom options to the encoder using kwargs.
# A ValueError is raised in case of failure.
s = d.to_toml(filepath='', **kwargs)
```

-   ##### to_yaml

```python
# Return the dict instance encoded in yaml format and optionally save it at the specified filepath.
# It's possible to pass custom options to the encoder using kwargs.
# A ValueError is raised in case of failure.
s = d.to_yaml(filepath='', **kwargs)
```

#### Parse
These methods are wrappers of the `get` method, they parse data trying to return it in the expected type.

-   ##### get_bool

```python
# Get value by key or keypath trying to return it as bool.
# Values like `1`, `true`, `yes`, `on`, `ok` will be returned as `True`.
d.get_bool(key, default=False)
```

-   ##### get_bool_list

```python
# Get value by key or keypath trying to return it as list of bool values.
# If separator is specified and value is a string it will be splitted.
d.get_bool_list(key, default=[], separator=',')
```

-   ##### get_datetime

```python
# Get value by key or keypath trying to return it as datetime.
# If format is not specified it will be autodetected.
# If options and value is in options return value otherwise default.
d.get_datetime(key, default=None, format=None, options=[])
```

-   ##### get_datetime_list

```python
# Get value by key or keypath trying to return it as list of datetime values.
# If separator is specified and value is a string it will be splitted.
d.get_datetime_list(key, default=[], format=None, separator=',')
```

-   ##### get_decimal

```python
# Get value by key or keypath trying to return it as Decimal.
# If options and value is in options return value otherwise default.
d.get_decimal(key, default=Decimal('0.0'), options=[])
```

-   ##### get_decimal_list

```python
# Get value by key or keypath trying to return it as list of Decimal values.
# If separator is specified and value is a string it will be splitted.
d.get_decimal_list(key, default=[], separator=',')
```

-   ##### get_dict

```python
# Get value by key or keypath trying to return it as dict.
# If value is a json string it will be automatically decoded.
d.get_dict(key, default={})
```

-   ##### get_email

```python
# Get email by key or keypath and return it.
# If value is blacklisted it will be automatically ignored.
# If check_blacklist is False, it will be not ignored even if blacklisted.
d.get_email(key, default='', options=None, check_blacklist=True)
```

-   ##### get_float

```python
# Get value by key or keypath trying to return it as float.
# If options and value is in options return value otherwise default.
d.get_float(key, default=0.0, options=[])
```

-   ##### get_float_list

```python
# Get value by key or keypath trying to return it as list of float values.
# If separator is specified and value is a string it will be splitted.
d.get_float_list(key, default=[], separator=',')
```

-   ##### get_int

```python
# Get value by key or keypath trying to return it as int.
# If options and value is in options return value otherwise default.
d.get_int(key, default=0, options=[])
```

-   ##### get_int_list

```python
# Get value by key or keypath trying to return it as list of int values.
# If separator is specified and value is a string it will be splitted.
d.get_int_list(key, default=[], separator=',')
```

-   ##### get_list

```python
# Get value by key or keypath trying to return it as list.
# If separator is specified and value is a string it will be splitted.
d.get_list(key, default=[], separator=',')
```

-   ##### get_list_item

```python
# Get list by key or keypath and return value at the specified index.
# If separator is specified and list value is a string it will be splitted.
d.get_list_item(key, index=0, default=None, separator=',')
```

-   ##### get_phonenumber

```python
# Get phone number by key or keypath and return a dict with different formats (e164, international, national).
# If country code is specified (alpha 2 code), it will be used to parse phone number correctly.
d.get_phonenumber(key, country_code=None, default=None)
```

-   ##### get_slug

```python
# Get value by key or keypath trying to return it as slug.
# If options and value is in options return value otherwise default.
d.get_slug(key, default='', options=[])
```

-   ##### get_slug_list

```python
# Get value by key or keypath trying to return it as list of slug values.
# If separator is specified and value is a string it will be splitted.
d.get_slug_list(key, default=[], separator=',')
```

-   ##### get_str

```python
# Get value by key or keypath trying to return it as string.
# Encoding issues will be automatically fixed.
# If options and value is in options return value otherwise default.
d.get_str(key, default='', options=[])
```

-   ##### get_str_list

```python
# Get value by key or keypath trying to return it as list of str values.
# If separator is specified and value is a string it will be splitted.
d.get_str_list(key, default=[], separator=',')
```

#### Utility
These methods are common utilities that will speed up your everyday work.

-   ##### clean

```python
# Clean the current dict removing all empty values: None, '', {}, [], ().
# If strings, dicts or lists flags are False, related empty values will not be deleted.
d.clean(strings=True, dicts=True, lists=True)
```

-   ##### clone

```python
# Return a clone (deepcopy) of the dict.
d.clone()
```

-   ##### dump

```python
# Return a readable representation of any dict/list.
# This method can be used both as static method or instance method.
s = benedict.dump(d.keypaths())
print(s)
# or
d = benedict()
print(d.dump())
```

-   ##### filter

```python
# Return a filtered dict using the given predicate function.
# Predicate function receives key, value arguments and should return a bool value.
predicate = lambda k, v: v is not None
d.filter(predicate)
```

-   ##### flatten

```python
# Return a flatten dict using the given separator to concat nested dict keys.
d.flatten(separator='_')
```

-   ##### merge

```python
# Merge one or more dictionary objects into current instance (deepupdate).
# Sub-dictionaries keys will be merged toghether.
d.merge(a, b, c)
```

-   ##### remove

```python
# Remove multiple keys from the dict.
d.remove(['firstname', 'lastname', 'email'])
```

-   ##### subset

```python
# Return a dict subset for the given keys.
d.subset(['firstname', 'lastname', 'email'])
```

## Testing
-   Run `tox` / `python setup.py test`

## License
Released under [MIT License](LICENSE.txt).