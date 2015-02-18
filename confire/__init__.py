# confire
# A simple app configuration scheme using YAML and class based defaults.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 20 09:44:32 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
A simple app configuration scheme using YAML and class based defaults.
"""

##########################################################################
## Imports
##########################################################################

from .config import Configuration, environ_setting
from .exceptions import ImproperlyConfigured

##########################################################################
## Module Info
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 2,
    'micro': 1,
    'releaselevel': 'final',
    'serial': 0,
}


def get_version(short=False):
    """
    Prints the version.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)

##########################################################################
## Package Version
##########################################################################

__version__ = get_version()
