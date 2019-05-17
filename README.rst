|Build Status| |codecov| |Code Health| |Requirements Status|
|PyPI version| |PyPI downloads| |Py versions| |License|

python-benedict
===============

python-benedict is the Python dictionary that helps humans dealing with
evil data.

Features
--------

-  Full **keypath** support *(using the dot syntax)*
-  Many **utility methods** to retrieve data as needed *(all methods
   listed below)*

Requirements
------------

-  Python 3.4, 3.5, 3.6, 3.7

Installation
------------

-  Run ``pip install python-benedict``

Testing
-------

-  Run ``tox`` / ``python setup.py test``

Usage
-----

``benedict`` is a dict subclass, so it is possible to use it as a normal
dict *(you can just cast an existing dict)*.

Basic get/set using keypath:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from benedict import benedict

    d = benedict()
    d['profile.firstname'] = 'Fabio'
    d['profile.lastname'] = 'Caccamo'
    print(d) # -> { 'profile':{ 'firstname':'Fabio', 'lastname':'Caccamo' } }
    print(d['profile']) # -> { 'firstname':'Fabio', 'lastname':'Caccamo' }
    print('profile.lastname' in d) # -> True

Utility methods:
^^^^^^^^^^^^^^^^

.. code:: python

    # Get value by key or keypath trying to return it as bool.
    # Values like `1`, `true`, `yes`, `on` will be returned as `True`.
    d.get_bool(key, default=False)

.. code:: python

    # Get value by key or keypath trying to return it as list of bool values.
    # If separator is specified and value is a string it will be splitted.
    d.get_bool_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as datetime.
    # If format is not specified it will be autodetected.
    # If options and value is in options return value otherwise default.
    d.get_datetime(key, default=None, format=None, options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of datetime values.
    # If separator is specified and value is a string it will be splitted.
    d.get_datetime_list(key, default=[], format=None, separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as Decimal.
    # If options and value is in options return value otherwise default.
    d.get_decimal(key, default=Decimal('0.0'), options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of Decimal values.
    # If separator is specified and value is a string it will be splitted.
    d.get_decimal_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as dict.
    # If value is a json string it will be automatically decoded.
    d.get_dict(key, default={})

.. code:: python

    # Get value by key or keypath trying to return it as float.
    # If options and value is in options return value otherwise default.
    d.get_float(key, default=0.0, options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of float values.
    # If separator is specified and value is a string it will be splitted.
    d.get_float_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as int.
    # If options and value is in options return value otherwise default.
    d.get_int(key, default=0, options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of int values.
    # If separator is specified and value is a string it will be splitted.
    d.get_int_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as list.
    # If separator is specified and value is a string it will be splitted.
    d.get_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as slug.
    # If options and value is in options return value otherwise default.
    d.get_slug(key, default='', options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of slug values.
    # If separator is specified and value is a string it will be splitted.
    d.get_slug_list(key, default=[], separator=',')

.. code:: python

    # Get value by key or keypath trying to return it as string.
    # Encoding issues will be automatically fixed.
    # If options and value is in options return value otherwise default.
    d.get_str(key, default='', options=[])

.. code:: python

    # Get value by key or keypath trying to return it as list of str values.
    # If separator is specified and value is a string it will be splitted.
    d.get_str_list(key, default=[], separator=',')

License
-------

Released under `MIT License <LICENSE.txt>`__.

.. |Build Status| image:: https://travis-ci.org/fabiocaccamo/python-benedict.svg?branch=master
   :target: https://travis-ci.org/fabiocaccamo/python-benedict
.. |codecov| image:: https://codecov.io/gh/fabiocaccamo/python-benedict/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/fabiocaccamo/python-benedict
.. |Code Health| image:: https://landscape.io/github/fabiocaccamo/python-benedict/master/landscape.svg?style=flat
   :target: https://landscape.io/github/fabiocaccamo/python-benedict/master
.. |Requirements Status| image:: https://requires.io/github/fabiocaccamo/python-benedict/requirements.svg?branch=master
   :target: https://requires.io/github/fabiocaccamo/python-benedict/requirements/?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/python-benedict.svg
   :target: https://badge.fury.io/py/python-benedict
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/python-benedict.svg
   :target: https://img.shields.io/pypi/dm/python-benedict.svg
.. |Py versions| image:: https://img.shields.io/pypi/pyversions/python-benedict.svg
   :target: https://img.shields.io/pypi/pyversions/python-benedict.svg
.. |License| image:: https://img.shields.io/pypi/l/python-benedict.svg
   :target: https://img.shields.io/pypi/l/python-benedict.svg
