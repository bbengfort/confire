# tests.paths_tests
# Testing the paths descriptor
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Jun 11 08:09:40 2015 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: paths_tests.py [] benjamin@bengfort.com $

"""
Testing the paths descriptor
"""

##########################################################################
## Imports
##########################################################################

import os
import shutil
import warnings
import unittest
import tempfile

from confire import path_setting
from confire.paths import Path
from confire.exceptions import ImproperlyConfigured, PathNotFound

##########################################################################
## Temporary Paths
##########################################################################

TEMPDIR = tempfile.mkdtemp('_paths', 'confire_')    # The base temporary directory
MDROOT  = os.path.join(TEMPDIR, "missing")          # The root of the missing directory, for unlinking
MISSDIR = os.path.join(MDROOT, "path", "to", "dir") # A temporary directory that does not exist
VARSDIR = tempfile.mkdtemp("subdir", dir=TEMPDIR)   # A temporary directory referenced by environment
TESTDIR = tempfile.mkdtemp("testdir", dir=TEMPDIR)  # Another temporary directory for testing

ENVVAR  = "VARDIR"  # environment variable to test expansion

##########################################################################
## Setup and tear down module
##########################################################################

def setUpModule():
    """
    Instantiates the environment variable
    """
    os.environ[ENVVAR] = VARSDIR

def tearDownModule():
    """
    Deletes temporary directories and paths for cleanup
    """
    shutil.rmtree(TEMPDIR)
    for path in (TEMPDIR, MISSDIR, VARSDIR):
        assert not os.path.exists(path)

##########################################################################
## Mock configuration object
##########################################################################

class TestObject(object):
    """
    Tests an object that has Path descriptors set on the class.
    """

    standard_path = Path()
    default_path  = Path('/tmp/paths/test')

##########################################################################
## Test case
##########################################################################

class PathsTests(unittest.TestCase):

    @classmethod
    def setUpClass(klass):
        for path in (TEMPDIR, VARSDIR):
            assert os.path.exists(path)

    def setUp(self):
        """
        Configures the test object instance
        """
        self.obj = TestObject()
        assert not os.path.exists(MISSDIR)

    def tearDown(self):
        """
        Deletes the test object instance and cleans up test directories
        """
        del self.obj
        if os.path.exists(MDROOT):
            shutil.rmtree(MDROOT)

    def test_set_and_get_paths(self):
        """
        Assert that paths can be set and got
        """

        paths = (
            'standard_path',
            'default_path',
        )

        for name in paths:
            setattr(self.obj, name, TESTDIR)
            attr = getattr(self.obj, name)

            self.assertEqual(attr, TESTDIR)
