# confire.descriptors
# Implements a base SettingsDescriptor for advanced configurations
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 11 09:34:33 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: descriptors.py [] benjamin@bengfort.com $

"""
Implements a base SettingsDescriptor for advanced configurations
"""

##########################################################################
## SettingsDescriptor object
##########################################################################

class SettingsDescriptor(object):
    """
    A standard descriptor for settings properties that require more advanced
    introspection, e.g. checking if a property is required or not. This is a
    base class that implements a very simple labeling property mechanism.

    Subclasses should take advantage of overriding methods as required.

    Note that a labeling Metaclass is required on the Configuration object.
    """

    def __init__(self):
        self.label = None

    def __get__(self, instance, owner):
        if not instance:
            return self

        if self.label is None:
            raise TypeError(
                "Objects that use SettingsDescriptors must use "
                "the SettingsMeta as their __metaclass__!"
            )

        return instance.__dict__.get(self.label, None)

    def __set__(self, instance, value):
        if self.label is None:
            raise TypeError(
                "Objects that use SettingsDescriptors must use "
                "the SettingsMeta as their __metaclass__!"
            )

        instance.__dict__[self.label] = value

    def __delete__(self, instance):
        if self.label is None:
            raise TypeError(
                "Objects that use SettingsDescriptors must use "
                "the SettingsMeta as their __metaclass__!"
            )

        del instance.__dict__[self.label]

##########################################################################
## Settings Meta Class
##########################################################################

class SettingsMeta(type):
    """
    Required metaclass for Configuration objects now.
    """

    def __new__(cls, name, bases, attrs):
        """
        Find all SettingsDescriptor subclasses and label them.
        """
        for n, v in attrs.items():
            if isinstance(v, SettingsDescriptor):
                v.label = n
        return super(SettingsMeta, cls).__new__(cls, name, bases, attrs)
