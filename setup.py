#!/usr/bin/env python
# setup
# Setup script for confire
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 20 11:06:56 2014 -0400
#
# Copyright (C) 2014-2015 Benjamin Bengfort
# For license information, see LICENSE.txt
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setup script for confire
"""

##########################################################################
## Imports
##########################################################################

import os
import codecs

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

PROJECT      = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = "requirements.txt"
TEST_REQUIRE_PATH = "tests/requirements.txt"
EXCLUDES = ("tests", "bin", "docs", "fixtures", "register",)

VERSION  = __import__('confire').__version__

## Discover the packages
PACKAGES = find_packages(where=".", exclude=EXCLUDES)

## Define the classifiers
CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
)

## Define the keywords
KEYWORDS = ('configuration', 'yaml', 'config', 'confire')

## Define the description
DESCRIPTION = (
    "Confire is a simple but powerful configuration scheme that builds on the "
    "configuration parsers of Scapy, elasticsearch, Django and others. The "
    "basic scheme is to have a configuration search path that looks for YAML "
    "files in standard locations. The search path is hierarchical (meaning "
    "that system configurations are overloaded by user configurations, etc). "
    "These YAML files are then added to a default, class-based configuration "
    "management scheme that allows for easy development.\n\n"
    "Documentation is available here: "
    "http://confire.readthedocs.org/en/latest/"
)

##########################################################################
## HELPER FUNCTIONS
##########################################################################

def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts), 'rb', 'utf-8') as f:
        return f.read()


def get_requires(path=REQUIRE_PATH):
    """
    Yields a generator of requirements as defined by the REQUIRE_PATH which
    should point to a requirements.txt output by `pip freeze`.
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            yield line

##########################################################################
## Define the configuration
##########################################################################

config = {
    "name": "confire",
    "version": VERSION,
    "description": "A simple app configuration scheme using YAML and class based defaults.",
    "long_description": DESCRIPTION,
    "license": "MIT License",
    "author": "Benjamin Bengfort",
    "author_email": "benjamin@bengfort.com",
    "url": "https://github.com/bbengfort/confire",
    "download_url": 'https://github.com/bbengfort/confire/tarball/v{}'.format(VERSION),
    "packages": PACKAGES,
    "install_requires": list(get_requires()),
    "setup_requires": ['pytest-runner'],
    "tests_require": list(get_requires(TEST_REQUIRE_PATH)),
    "classifiers": CLASSIFIERS,
    "keywords": KEYWORDS,
    "zip_safe": True,
    "scripts": [],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
