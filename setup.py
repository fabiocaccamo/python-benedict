#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

import os

exec(open('benedict/metadata.py').read())

github_url = 'https://github.com/fabiocaccamo'
package_name = 'python-benedict'
package_path = os.path.abspath(os.path.dirname(__file__))
long_description_file_path = os.path.join(package_path, 'README.rst')
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
    author=__author__,
    author_email='fabio.caccamo@gmail.com',
    url='%s/%s' % (github_url, package_name, ),
    download_url='%s/%s/archive/%s.tar.gz' % (github_url, package_name, __version__, ),
    keywords=['benedict', 'python', 'dict', 'keypath', 'parse', 'utility'],
    install_requires=[
        'ftfy',             # >= 5.0.0, < 6.0.0;
        'python-dateutil',  # >= 2.6.0, < 3.0.0',
        'python-slugify',   # >= 1.2.0, < 4.0.0',
        # 'pyyaml',
        # 'xmltodict',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Build Tools',
    ],
    license='MIT',
    test_suite='tests'
)
