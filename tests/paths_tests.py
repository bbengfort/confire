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

from six import with_metaclass
from confire.paths import Path
from confire import path_setting
from confire.descriptors import SettingsMeta
from confire.exceptions import ImproperlyConfigured, PathNotFound

##########################################################################
## Temporary Paths
##########################################################################

TEMPDIR  = tempfile.mkdtemp('_paths', 'confire_')    # The base temporary directory
MDROOT   = os.path.join(TEMPDIR, "missing")          # The root of the missing directory, for unlinking
MISSDIR  = os.path.join(MDROOT, "path", "to", "dir") # A temporary directory that does not exist
VARSDIR  = tempfile.mkdtemp("subdir", dir=TEMPDIR)   # A temporary directory referenced by environment
TESTDIR  = tempfile.mkdtemp("testdir", dir=TEMPDIR)  # Another temporary directory for testing
_, TESTFILE = tempfile.mkstemp("test.txt", dir=TEMPDIR) # A temporary file for testing

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
    for path in (TEMPDIR, MISSDIR, VARSDIR, TESTDIR, TESTFILE):
        assert not os.path.exists(path)

##########################################################################
## Mock configuration object
##########################################################################

class TestObject(with_metaclass(SettingsMeta, object)):
    """
    Tests an object that has Path descriptors set on the class.
    """

    __metaclass__ = SettingsMeta

    standard_path     = path_setting()
    default_path      = path_setting(default=TESTDIR)
    not_required_path = path_setting(required=False)
    mkdirs_path       = path_setting(mkdirs=True)
    mk_no_raise_path  = path_setting(mkdirs=True, raises=False)
    dont_raise_path   = path_setting(raises=False)
    not_absolute      = path_setting(absolute=False, raises=False)
    silent_path       = path_setting(raises=False, required=False)


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

        self.path_attrs = (
            'standard_path',
            'default_path',
            'not_required_path',
            'mkdirs_path',
            'mk_no_raise_path',
            'dont_raise_path',
            'not_absolute',
            'silent_path',
        )


    def tearDown(self):
        """
        Deletes the test object instance and cleans up test directories
        """
        del self.obj
        if os.path.exists(MDROOT):
            shutil.rmtree(MDROOT)

        # Delete contents of the test file
        with open(TESTFILE, 'w') as f:
            pass

    def test_label(self):
        """
        Check that path settings get labeled
        """
        for name in self.path_attrs:
            setting = getattr(TestObject, name)
            self.assertEqual(setting.label, name)

    def test_get_path_descriptor(self):
        """
        Check that the path descriptor can be fetched from the class
        """
        self.assertTrue(isinstance(TestObject.default_path, Path))
        self.assertTrue(isinstance(self.obj.default_path, basestring))

    def test_set_and_get_paths(self):
        """
        Assert that paths can be set and fetched
        """

        for name in self.path_attrs:
            setattr(self.obj, name, TESTDIR)
            attr = getattr(self.obj, name)

            self.assertEqual(attr, TESTDIR)

    def test_delete_not_required_path(self):
        """
        Assert that paths can be deleted
        """
        # Must use the not required path, otherwise exceptions!
        self.obj.not_required_path = TESTDIR
        self.assertEqual(self.obj.not_required_path, TESTDIR)

        del self.obj.not_required_path
        self.assertIsNone(self.obj.not_required_path)

    def test_delete_required_path(self):
        """
        Test that required paths on delete raise error
        """
        with self.assertRaises(ImproperlyConfigured):
            # Path is required on access
            path = self.obj.standard_path

        # Set to a file, and we're good to go
        self.obj.standard_path = TESTFILE
        path = self.obj.standard_path
        self.assertEqual(path, TESTFILE)

        # Now try to delete it
        del self.obj.standard_path
        with self.assertRaises(ImproperlyConfigured):
            path = self.obj.standard_path

    def test_default_path(self):
        """
        Check that a default path is returned when not set
        """

        # Make sure the default is available
        self.assertIsNotNone(self.obj.default_path)
        self.assertEqual(self.obj.default_path, TESTDIR)

        # Change the default to the test file
        self.obj.default_path = TESTFILE
        self.assertEqual(self.obj.default_path, TESTFILE)

        # Now delete the test file and check default again
        del self.obj.default_path
        self.assertIsNotNone(self.obj.default_path)
        self.assertEqual(self.obj.default_path, TESTDIR)

    def test_required_path(self):
        """
        Assert that paths are required
        """
        with self.assertRaises(ImproperlyConfigured):
            path = self.obj.standard_path

    def test_not_required_path(self):
        """
        Assert not required paths don't raise an error
        """
        try:
            path = self.obj.not_required_path
            self.assertIsNone(path)
        except ImproperlyConfigured:
            self.fail("Not required path raised a configuration error")

    @unittest.skip("warning not triggered in test?")
    def test_path_not_found_warning(self):
        """
        Test that PathNotFound is warned on not raises
        """
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")

            self.assertFalse(TestObject.dont_raise_path.mkdirs)
            self.assertFalse(os.path.exists(MISSDIR))

            # Trigger a warning.
            self.dont_raise_path = MISSDIR

            # Verify some things
            assert len(w) == 1
            assert issubclass(w[-1].category, PathNotFound)

    def test_user_expansion(self):
        """
        Test that on set, user is expanded.
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            # Use the not raises so that we don't have to create the user path
            testpath = "~/path/to/test"
            self.obj.dont_raise_path = "~/path/to/test"
            self.assertEqual(self.obj.dont_raise_path, os.path.expanduser(testpath))


    def test_vars_expansion(self):
        """
        Test that on set, vars are expanded.
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            self.obj.standard_path = "${}".format(ENVVAR)
            self.assertEqual(self.obj.standard_path, VARSDIR)

    def test_normpath_path(self):
        """
        Test that on set the path is normed
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            # Use the not raises so that we don't have to create the user path
            path = os.path.join(VARSDIR, "..")
            self.obj.standard_path = path
            self.assertEqual(self.obj.standard_path, TEMPDIR)

    def test_absolute_path(self):
        """
        Test that the path is transformed into an absolute path
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            # Use the not raises so that we don't have to create the user path
            relative_path = "path/to/test.txt"
            self.obj.dont_raise_path = relative_path
            self.assertEqual(self.obj.dont_raise_path, os.path.abspath(relative_path))

    def test_not_absolute_path(self):
        """
        Test that the path is not transformed into an absolute path
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            # Use the not raises so that we don't have to create the user path
            relative_path = "path/to/test.txt"
            self.obj.not_absolute = relative_path
            self.assertEqual(self.obj.not_absolute, relative_path)

    def test_mkdirs_path(self):
        """
        Test that a directory is created on mkdirs = True
        """
        self.assertFalse(os.path.exists(MISSDIR))
        self.obj.mkdirs_path = MISSDIR
        self.assertTrue(os.path.exists(MISSDIR))

    def test_no_mkdirs_path(self):
        """
        Test that no directory is created by default
        """
        with warnings.catch_warnings():
            # There will be warnings, just ignore them
            warnings.simplefilter("ignore")

            self.assertFalse(os.path.exists(MISSDIR))
            self.obj.silent_path = MISSDIR
            self.assertFalse(os.path.exists(MISSDIR))

    def test_raises_path(self):
        """
        Test that if raises is True, an exception happens
        """
        for path in ('standard_path', 'default_path', 'not_required_path'):
            with self.assertRaises(ImproperlyConfigured):
                self.assertFalse(os.path.exists(MISSDIR))
                setattr(self.obj, path, MISSDIR)

    def test_not_raises_path(self):
        """
        Assert other paths don't raise an exception
        """
        for path in ('mk_no_raise_path', 'dont_raise_path', 'not_absolute', 'silent_path'):
            try:
                if os.path.exists(MISSDIR):
                    shutil.rmtree(MISSDIR)

                setattr(self.obj, path, MISSDIR)
            except ImproperlyConfigured:
                self.fail("Improperly configured raised on %s" % path)
