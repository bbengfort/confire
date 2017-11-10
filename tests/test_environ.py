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
import pytest

from confire import environ_setting
from confire.exceptions import ImproperlyConfigured, ConfigurationMissing


##########################################################################
## Fixtures
##########################################################################

ENVKEY = 'TEST_SETTING'
ENVVAL = '42'

@pytest.fixture(scope='function')
def environ():
    os.environ[ENVKEY] = ENVVAL
    yield
    os.environ.pop(ENVKEY)
    assert ENVKEY not in os.environ


##########################################################################
## Test case
##########################################################################

class TestEnviron(object):

    def test_environ_setting(self, environ):
        """
        Test settings can be grabbed from environment
        """
        assert ENVVAL == environ_setting(ENVKEY)
        assert ENVVAL == environ_setting(ENVKEY, default='15')
        assert ENVVAL == environ_setting(ENVKEY, required=False)
        assert ENVVAL == environ_setting(ENVKEY, default='15', required=False)

    def test_improperly_configured(self):
        """
        Test that ImproperlyConfigured is raised on missing setting
        """
        FAKEKEY = 'MISSING_SETTING'
        with pytest.raises(ImproperlyConfigured):
            environ_setting(FAKEKEY)

    def test_configuration_missing(self):
        """
        Test that ConfigurationMissing is warned on missing setting
        """
        FAKEKEY = 'MISSING_SETTING'
        with pytest.warns(ConfigurationMissing):
            environ_setting(FAKEKEY, required=False)

    def test_environ_default(self):
        """
        Test that a default is returned on required
        """
        FAKEKEY = 'MISSING_SETTING'
        assert environ_setting(FAKEKEY, default='15') == '15'

    @pytest.mark.filterwarnings("ignore")
    def test_environ_default_none(self):
        """
        Test that None is returned on not required
        """
        FAKEKEY = 'MISSING_SETTING'
        assert environ_setting(FAKEKEY, required=False) is None

    def test_enivron_default_other(self):
        """
        Test that a default is returned on not required
        """
        FAKEKEY = 'MISSING_SETTING'
        assert environ_setting(FAKEKEY, required=False, default='15') == '15'
