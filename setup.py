#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os, sys

exec(open('benedict/metadata.py').read())

github_url = 'https://github.com/fabiocaccamo'
package_name = 'python-benedict'
package_url = '{}/{}'.format(github_url, package_name)
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.md')
long_description_content_type = 'text/markdown'
long_description = ''
try:
    long_description_file_options = {} if sys.version_info[0] < 3 else { 'encoding':'utf-8' }
    with open(long_description_file_path, 'r', **long_description_file_options) as f:
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
        'configparser', 'config', 'cfg', 'pickle', 'plist',
        'base64', 'csv', 'ini', 'json', 'query-string', 'toml', 'xml', 'yaml',
        'clean', 'clone', 'deepclone', 'deepupdate', 'dump',
        'filter', 'flatten', 'groupby', 'invert', 'merge',
        'move', 'nest', 'remove', 'rename', 'search', 'standardize',
        'subset', 'swap', 'traverse', 'unflatten', 'unique',
    ],
    install_requires=[
        'ftfy == 4.4.3; python_version <= "2.7"',
        'ftfy == 5.9.0; python_version == "3.5"',
        'ftfy; python_version >= "3.6"',
        'mailchecker',
        'phonenumbers',
        'python-dateutil',
        'python-fsutil',
        'python-slugify',
        'pyyaml',
        'requests',
        'six',
        'toml',
        'xmltodict',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: MacOS X',
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Education :: Testing',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Filesystems',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',
    ],
    license=__license__,
    test_suite='tests'
)
