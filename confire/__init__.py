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
## Package constants
##########################################################################

__version__ = (0, 2, 0)

def get_version():
    """
    Returns a string containing the version number
    """
    return ".".join("%i" % idx for idx in __version__)
