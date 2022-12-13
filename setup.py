#!/usr/bin/env python

import os

from setuptools import find_packages, setup

exec(open("benedict/metadata.py").read())

package_name = "python-benedict"
package_url = f"https://github.com/fabiocaccamo/{package_name}"
package_path = os.path.abspath(os.path.dirname(__file__))
download_url = f"{package_url}/archive/{__version__}.tar.gz"
documentation_url = f"{package_url}#readme"
issues_url = f"{package_url}/issues"
sponsor_url = "https://github.com/sponsors/fabiocaccamo/"
twitter_url = "https://twitter.com/fabiocaccamo"

long_description_file_path = os.path.join(package_path, "README.md")
long_description_content_type = "text/markdown"
long_description = ""
try:
    with open(long_description_file_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name=package_name,
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author=__author__,
    author_email=__email__,
    url=package_url,
    download_url=download_url,
    project_urls={
        "Documentation": documentation_url,
        "Issues": issues_url,
        "Funding": sponsor_url,
        "Twitter": twitter_url,
    },
    keywords=[
        "python",
        "dictionary",
        "dictionaries",
        "dict",
        "benedict",
        "subclass",
        "extended",
        "keylist",
        "keypath",
        "utility",
        "io",
        "data",
        "file",
        "url",
        "read",
        "write",
        "parse",
        "configparser",
        "config",
        "cfg",
        "pickle",
        "plist",
        "base64",
        "csv",
        "ini",
        "json",
        "query-string",
        "toml",
        "xml",
        "yaml",
        "clean",
        "clone",
        "deepclone",
        "deepupdate",
        "dump",
        "filter",
        "flatten",
        "groupby",
        "invert",
        "merge",
        "move",
        "nest",
        "remove",
        "rename",
        "search",
        "standardize",
        "subset",
        "swap",
        "traverse",
        "unflatten",
        "unique",
    ],
    install_requires=[
        "boto3 >= 1.24.89, < 2.0.0",
        "ftfy >= 6.0.0, < 7.0.0",
        "mailchecker >= 4.1.0, < 6.0.0",
        "openpyxl >= 3.0.0, < 4.0.0",
        "phonenumbers >= 8.12.0, < 9.0.0",
        "python-dateutil >= 2.8.0, < 3.0.0",
        "python-fsutil >= 0.6.0, < 1.0.0",
        "python-slugify >= 6.0.1, < 8.0.0",
        "pyyaml >= 6.0, < 7.0",
        "requests >= 2.26.0, < 3.0.0",
        "toml >= 0.10.2, < 1.0.0",
        "xlrd >= 2.0.0, < 3.0.0",
        "xmltodict >= 0.12.0, < 1.0.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education :: Testing",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Filesystems",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Utilities",
    ],
)
