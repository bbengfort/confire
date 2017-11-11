# tests.test_descriptors
# Implements a base SettingsDescriptor for advanced configurations
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 11 09:34:33 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: test_descriptors.py [] benjamin@bengfort.com $

"""
Implements a base SettingsDescriptor for advanced configurations
"""

##########################################################################
## Imports
##########################################################################

import pytest

from six import with_metaclass
from confire.descriptors import SettingsDescriptor, SettingsMeta


##########################################################################
## Mock Objects for Testing
##########################################################################

class MockObject(with_metaclass(SettingsMeta, object)):

    test_setting = SettingsDescriptor()


class BadMockObject(object):
    """
    Missing metaclass!
    """

    test_setting = SettingsDescriptor()


##########################################################################
## Test Cases
##########################################################################

class TestDescriptors(object):

    def test_label(self):
        """
        Assert that descriptor label is not None
        """
        assert MockObject.test_setting.label is not None
        assert MockObject.test_setting.label == "test_setting"

    def test_descriptor_set_get(self):
        """
        Test that the descriptor can be set and fetched
        """
        obj = MockObject()
        assert obj.test_setting is None
        obj.test_setting = "foo"
        assert obj.test_setting == "foo"

    def test_descriptor_set_get_dict(self):
        """
        Test that the descriptor is in the instance dict
        """
        obj = MockObject()
        assert obj.__dict__.get('test_setting') is None
        obj.test_setting = "foo"
        assert obj.__dict__.get('test_setting') == "foo"

    def test_descriptor_del(self):
        """
        Test that the descriptor can be deleted
        """

        obj = MockObject()
        assert obj.test_setting is None
        obj.test_setting = "foo"
        assert obj.test_setting is not None
        del obj.test_setting
        assert obj.test_setting is None

    def test_descriptor_del_dict(self):
        """
        Test that the descriptor removes information from instance dict
        """
        obj = MockObject()
        assert obj.__dict__.get('test_setting') is None
        obj.test_setting = "foo"
        assert obj.__dict__.get('test_setting') is not None
        del obj.test_setting
        assert 'test_setting' not in obj.__dict__

    def test_no_metaclass_get(self):
        """
        Test getattr when object doesn't have a metaclass
        """
        obj = BadMockObject()
        with pytest.raises(TypeError):
            obj.test_setting

    def test_no_metaclass_set(self):
        """
        Test setattr when object doesn't have a metaclass
        """
        obj = BadMockObject()
        with pytest.raises(TypeError):
            obj.test_setting = "foo"

    def test_no_metaclass_del(self):
        """
        Test delattr when object doesn't have a metaclass
        """
        obj = BadMockObject()
        with pytest.raises(TypeError):
            del obj.test_setting

    def test_subclass_with_metaclass(self):
        """
        Ensure that subclasses also have metaclass
        """

        class SubMockObject(MockObject):

            subtest_setting = SettingsDescriptor()

        assert SubMockObject.test_setting.label is not None
        assert SubMockObject.test_setting.label == "test_setting"
        assert SubMockObject.subtest_setting.label is not None
        assert SubMockObject.subtest_setting.label == "subtest_setting"
