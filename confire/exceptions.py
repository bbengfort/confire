# confire.exceptions
# Exceptions hierarchy for Confire
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Jul 21 11:02:09 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exceptions hierarchy for Confire
"""

##########################################################################
## Exceptions Hierarchy
##########################################################################

class ConfireException(Exception):
    """
    Base class for configuration exceptions.
    """
    pass

class ImproperlyConfigured(ConfireException):
    """
    The user did not properly set a configuration value.
    """
    pass

##########################################################################
## Warnings Hierarchy
##########################################################################

class ConfireWarning(Warning):
    """
    Base class for configuration warnings.
    """
    pass

class ConfigurationMissing(ConfireWarning):
    """
    Warn the user that an optional configuration is missing.
    """
    pass
