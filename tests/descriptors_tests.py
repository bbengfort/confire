# tests.descriptors_tests
# Implements a base SettingsDescriptor for advanced configurations
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 11 09:34:33 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: descriptors_tests.py [] benjamin@bengfort.com $

"""
Implements a base SettingsDescriptor for advanced configurations
"""

##########################################################################
## Imports
##########################################################################

import unittest

from confire.descriptors import SettingsDescriptor, SettingsMeta

##########################################################################
## Mock Objects for Testing
##########################################################################

class TestObject(object):

    __metaclass__ = SettingsMeta

    test_setting = SettingsDescriptor()


class BadTestObject(object):
    """
    Missing metaclass!
    """

    test_setting = SettingsDescriptor()

##########################################################################
## Test Case
##########################################################################


class DescriptorTests(unittest.TestCase):

    def test_label(self):
        """
        Assert that descriptor label is not None
        """
        self.assertIsNotNone(TestObject.test_setting.label)
        self.assertEqual(TestObject.test_setting.label, "test_setting")

    def test_descriptor_set_get(self):
        """
        Test that the descriptor can be set and fetched
        """
        obj = TestObject()
        self.assertIsNone(obj.test_setting)
        obj.test_setting = "foo"
        self.assertEqual(obj.test_setting, "foo")

    def test_descriptor_set_get_dict(self):
        """
        Test that the descriptor is in the instance dict
        """
        obj = TestObject()
        self.assertIsNone(obj.__dict__.get('test_setting'))
        obj.test_setting = "foo"
        self.assertEqual(obj.__dict__.get('test_setting'), "foo")

    def test_descriptor_del(self):
        """
        Test that the descriptor can be deleted
        """

        obj = TestObject()
        self.assertIsNone(obj.test_setting)
        obj.test_setting = "foo"
        self.assertIsNotNone(obj.test_setting)
        del obj.test_setting
        self.assertIsNone(obj.test_setting)

    def test_descriptor_del_dict(self):
        """
        Test that the descriptor removes information from instance dict
        """
        obj = TestObject()
        self.assertIsNone(obj.__dict__.get('test_setting'))
        obj.test_setting = "foo"
        self.assertIsNotNone(obj.__dict__.get('test_setting'))
        del obj.test_setting
        self.assertNotIn('test_setting', obj.__dict__)

    def test_no_metaclass_get(self):
        """
        Test getattr when object doesn't have a metaclass
        """
        obj = BadTestObject()
        with self.assertRaises(TypeError):
            x = obj.test_setting

    def test_no_metaclass_set(self):
        """
        Test setattr when object doesn't have a metaclass
        """
        obj = BadTestObject()
        with self.assertRaises(TypeError):
            obj.test_setting = "foo"

    def test_no_metaclass_get(self):
        """
        Test delattr when object doesn't have a metaclass
        """
        obj = BadTestObject()
        with self.assertRaises(TypeError):
            del obj.test_setting
