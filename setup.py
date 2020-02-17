#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os

exec(open('benedict/metadata.py').read())

github_url = 'https://github.com/fabiocaccamo'
package_name = 'python-benedict'
package_url = '{}/{}'.format(github_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.md')
long_description_content_type = 'text/markdown'
long_description = ''
try:
    with open(long_description_file_path) as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author=__author__,
    author_email=__email__,
    url=package_url,
    download_url='{}/archive/{}.tar.gz'.format(package_url, __version__),
    keywords=[
        'python', 'dictionary', 'dictionaries', 'dict', 'benedict',
        'subclass', 'extended', 'keylist', 'keypath', 'utility', 'io',
        'data', 'file', 'url', 'read', 'write', 'parse',
        'base64', 'csv', 'json', 'query-string', 'toml', 'xml', 'yaml',
        'clean', 'clone', 'deepclone', 'deepupdate', 'dump',
        'filter', 'flatten', 'groupby', 'invert', 'merge',
        'move', 'nest', 'remove', 'rename', 'search', 'standardize',
        'subset', 'swap', 'traverse', 'unflatten', 'unique',
    ],
    install_requires=[
        'ftfy==4.4.3;python_version<"3.4"',
        'ftfy;python_version>"2.7"',
        'mailchecker',
        'phonenumbers',
        'python-dateutil',
        'python-slugify',
        'pyyaml',
        'requests',
        'six',
        'toml',
        'xmltodict',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools',
    ],
    license=__license__,
    test_suite='tests'
)
