# tests.test_safety
# Test that we're using safe methods
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Nov 10 12:22:35 2017 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: test_safety.py [] benjamin@bengfort.com $

"""
Testing the paths descriptor
"""

##########################################################################
## Imports
##########################################################################

import os

from unittest import mock


# Cannot import from test_conf.py to ensure correct mock
TESTDATA = os.path.join(os.path.dirname(__file__), "testdata")
TESTCONF = os.path.join(TESTDATA, "testconf.yaml")


@mock.patch('confire.config.yaml')
def test_use_yaml_safe_load(mock_yaml):
    """
    Ensure we're using yaml.safe_load not yaml.load
    """
    from confire.config import Configuration
    Configuration.CONF_PATHS = [TESTCONF]
    Configuration.load()

    mock_yaml.safe_load.assert_called_once()
    mock_yaml.load.assert_not_called()
