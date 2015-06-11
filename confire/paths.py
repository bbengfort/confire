# confire.paths
# A descriptor for managing path properties and configurations
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 11 07:32:23 2015 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: paths.py [] benjamin@bengfort.com $

"""
A descriptor for managing path properties and configurations
"""

##########################################################################
## Imports
##########################################################################

import os
import warnings

from weakref import WeakKeyDictionary
from .exceptions import ImproperlyConfigured, PathNotFound

##########################################################################
## Path descriptor
##########################################################################

class Path(object):
    """
    Descriptor that enables the configuration of paths on the local file
    system. By default, the descriptor manages strings on set as follows:

        1. Expand user (e.g. ~)
        2. Expand vars (e.g. $HOME)
        3. Normalize the path (e.g. .. and . resolution)
        4. If absolute, return the absolute path

    If mkdirs is True, then this function will create the directory if it
    does not exist. If raises is True, then it will raise an exception if the
    directory does not exist. If required is True, then this will raise an
    exception if the path or the default is None.
    """

    def __init__(self, default=None, absolute=True, mkdirs=False, raises=True, required=True):
        self.label     = "confire path" # TODO: Implement SettingsDescriptor

        # Configuration of the descriptor
        self.default   = default     # If path is  None
        self.absolute  = absolute    # Convert to the abspath
        self.mkdirs    = mkdirs      # Create the directory if not exists
        self.raises    = raises      # Raise an exception if driectory not exists
        self.required  = required    # Raise an exception if value is None

        # The stored data for the descriptor
        self.paths     = WeakKeyDictionary()    # Stores computed paths by the above rules per instance
        self.strings   = WeakKeyDictionary()    # Stores the original string passed in per instance

    def __get__(self, obj, owner=None):
        if obj is None:
            # Accessed from the class, allow inspection
            return self

        path = self.paths.get(obj, self.default)

        if not path and self.required:
            raise ImproperlyConfigured(
                "The '{0}' Path configuration is not set".format(self.label)
            )

        return path

    def __set__(self, obj, value):
        # Store original
        self.strings[obj] = value

        # Compute the path
        value = os.path.expanduser(value)
        value = os.path.expandvars(value)
        value = os.path.normpath(value)

        if self.absolute:
            value = os.path.abspath(value)

        if self.mkdirs and not os.path.exists(value):
            os.makedirs(value)

        if not os.path.exists(value):
            message = "Path at '{0}' does not exist!".format(value)
            if self.raises:
                raise ImproperlyConfigured(message)
            else:
                warnings.warn(PathNotFound(message))

        self.paths[obj] = value

    def __delete__(self, obj):
        del self.paths[obj]
        del self.strings[obj]
