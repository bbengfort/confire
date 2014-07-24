# tests.environ_tests
# Tests the environment configuration ability
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Mon Jul 21 11:17:23 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: environ_tests.py [] benjamin@bengfort.com $

"""
Tests the environment configuration ability
"""

##########################################################################
## Imports
##########################################################################

import os
import warnings
import unittest

from confire import environ_setting
from confire.exceptions import ImproperlyConfigured, ConfigurationMissing

##########################################################################
## Test case
##########################################################################

class EnvironTests(unittest.TestCase):

    ENVKEY = 'TEST_SETTING'
    ENVVAL = '42'

    def setUp(self):
        os.environ[self.ENVKEY] = self.ENVVAL

    def tearDown(self):
        os.environ.pop(self.ENVKEY)
        assert self.ENVKEY not in os.environ

    def test_environ_setting(self):
        """
        Test settings can be grabbed from environment
        """
        self.assertEqual(self.ENVVAL, environ_setting(self.ENVKEY))
        self.assertEqual(self.ENVVAL, environ_setting(self.ENVKEY, default='15'))
        self.assertEqual(self.ENVVAL, environ_setting(self.ENVKEY, required=False))
        self.assertEqual(self.ENVVAL, environ_setting(self.ENVKEY, default='15', required=False))

    def test_improperly_configured(self):
        """
        Test that ImproperlyConfigured is raised on missing setting
        """
        FAKEKEY = 'MISSING_SETTING'
        with self.assertRaises(ImproperlyConfigured):
            environ_setting(FAKEKEY)

    def test_configuration_missing(self):
        """
        Test that ConfigurationMissing is warned on missing setting
        """
        FAKEKEY = 'MISSING_SETTING'
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            environ_setting(FAKEKEY, required=False)
            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, ConfigurationMissing)

    def test_environ_default(self):
        """
        Test that a default is returned on required
        """
        FAKEKEY = 'MISSING_SETTING'
        self.assertEqual('15', environ_setting(FAKEKEY, default='15'))

    def test_environ_default_none(self):
        """
        Test that None is returned on not required
        """
        FAKEKEY = 'MISSING_SETTING'
        self.assertIsNone(environ_setting(FAKEKEY, required=False))

    def test_enivron_default_other(self):
        """
        Test that a default is returned on not required
        """
        FAKEKEY = 'MISSING_SETTING'
        self.assertEqual('15', environ_setting(FAKEKEY, required=False, default='15'))
