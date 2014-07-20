#!/usr/bin/env python
# setup
# Setup script for confire
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 20 11:06:56 2014 -0400
#
# Copyright (C) 2014 District Data Labs
# For license information, see LICENSE.txt and NOTICE.md
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setup script for science-bookclub
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

packages = find_packages(where=".", exclude=("tests", "bin", "docs", "fixtures",))
requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
)

keywords = ('configuration', 'yaml', 'config', 'confire')

config = {
    "name": "confire",
    "version": "0.1.0",
    "description": "A simple app configuration scheme using YAML and class based defaults.",
    "license": "MIT",
    "author": "Benjamin Bengfort",
    "author_email": "benjamin@bengfort.com",
    "url": "https://github.com/bbengfort/confire",
    "download_url" = 'https://github.com/bbengfort/confire/tarball/v0.1.0'
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "keywords": keywords,
    "zip_safe": True,
    "scripts": [],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
