# python-benedict
python-benedict is the Python dictionary that helps humans dealing with evil data.

## Features
- Full *keypath* support *(using the dot syntax)*
- Many *utility methods* to retrieve data as needed easily

## Requirements
- Python 2.7, 3.4, 3.5, 3.6, 3.7

## Installation
- Run `pip install python-benedict`

## Usage
`benedict` is a dict subclass, so it is possible to use it as a normal dict *(you can just cast an existing dict)*.

#### Basic get/set using keypath:
All get/set operations provide keypath support *(using the dot syntax)*.

```python
from benedict import benedict

d = benedict()
d['profile.firstname'] = 'Fabio'
d['profile.lastname'] = 'Caccamo'
print(d) # -> { 'profile':{ 'firstname':'Fabio', 'lastname':'Caccamo' } }
print(d['profile']) # -> { 'firstname':'Fabio', 'lastname':'Caccamo' }
print('profile.lastname' in d) # -> True
```

#### Utility methods:

```python
"""
Get value by key or keypath trying to return it as bool.
Values like `1`, `true`, `yes`, `on` will be returned as `True`.
"""
d.get_bool(key, default=False)
```

```python
"""
Get value by key or keypath trying to return it as list of bool values.
If separator is specified and value is a string it will be splitted.
"""
d.get_bool_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as datetime.
If format is not specified it will be autodetected.
If options and value is in options return value otherwise default.
"""
d.get_datetime(key, default=None, format=None, options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of datetime values.
If separator is specified and value is a string it will be splitted.
"""
d.get_datetime_list(key, default=[], format=None, separator=',')
```

```python
"""
Get value by key or keypath trying to return it as Decimal.
If options and value is in options return value otherwise default.
"""
d.get_decimal(key, default=Decimal('0.0'), options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of Decimal values.
If separator is specified and value is a string it will be splitted.
"""
d.get_decimal_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as dict.
If value is a json string it will be automatically decoded.
"""
d.get_dict(key, default={})
```

```python
"""
Get value by key or keypath trying to return it as float.
If options and value is in options return value otherwise default.
"""
d.get_float(key, default=0.0, options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of float values.
If separator is specified and value is a string it will be splitted.
"""
d.get_float_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as int.
If options and value is in options return value otherwise default.
"""
d.get_int(key, default=0, options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of int values.
If separator is specified and value is a string it will be splitted.
"""
d.get_int_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as list.
If separator is specified and value is a string it will be splitted.
"""
d.get_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as slug.
If options and value is in options return value otherwise default.
"""
d.get_slug(key, default='', options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of slug values.
If separator is specified and value is a string it will be splitted.
"""
d.get_slug_list(key, default=[], separator=',')
```

```python
"""
Get value by key or keypath trying to return it as string.
Encoding issues will be automatically fixed.
If options and value is in options return value otherwise default.
"""
d.get_str(key, default='', options=[])
```

```python
"""
Get value by key or keypath trying to return it as list of str values.
If separator is specified and value is a string it will be splitted.
"""
d.get_str_list(key, default=[], separator=',')
```

## License
Released under [MIT License](LICENSE.txt).