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
import pytest
import shutil
import tempfile

from confire.paths import Path
from confire import path_setting
from six import with_metaclass, string_types
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

@pytest.fixture(scope='module', autouse=True)
def environ():
    os.environ[ENVVAR] = VARSDIR
    yield
    os.environ.pop(ENVVAR)


@pytest.fixture(scope='module', autouse=True)
def paths():
    for path in (TEMPDIR, VARSDIR):
        assert os.path.exists(path)
    yield
    shutil.rmtree(TEMPDIR)
    for path in (TEMPDIR, MISSDIR, VARSDIR, TESTDIR, TESTFILE):
        assert not os.path.exists(path)


@pytest.fixture(scope='function', autouse=True)
def destroy_paths():
    yield
    if os.path.exists(MDROOT):
        shutil.rmtree(MDROOT)

    # Delete contents of the test file
    with open(TESTFILE, 'w') as f:
        f.write("")


@pytest.fixture(scope='function')
def mockobj():
    obj = MockObject()
    path_attrs = (
        'standard_path',
        'default_path',
        'not_required_path',
        'mkdirs_path',
        'mk_no_raise_path',
        'dont_raise_path',
        'not_absolute',
        'silent_path',
    )
    return obj, path_attrs


##########################################################################
## Mock configuration object
##########################################################################

class MockObject(with_metaclass(SettingsMeta, object)):
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

class TestPaths():

    def test_label(self, mockobj):
        """
        Check that path settings get labeled
        """
        _, path_attrs = mockobj
        for name in path_attrs:
            setting = getattr(MockObject, name)
            assert setting.label == name

    def test_get_path_descriptor(self, mockobj):
        """
        Check that the path descriptor can be fetched from the class
        """
        obj,_ = mockobj
        assert isinstance(MockObject.default_path, Path)
        assert isinstance(obj.default_path, string_types)

    def test_set_and_get_paths(self, mockobj):
        """
        Assert that paths can be set and fetched
        """
        obj, path_attrs = mockobj
        for name in path_attrs:
            setattr(obj, name, TESTDIR)
            attr = getattr(obj, name)

            assert attr == TESTDIR

    def test_delete_not_required_path(self, mockobj):
        """
        Assert that paths can be deleted
        """
        obj, _ = mockobj

        # Must use the not required path, otherwise exceptions!
        obj.not_required_path = TESTDIR
        assert obj.not_required_path == TESTDIR

        del obj.not_required_path
        assert obj.not_required_path is None

    def test_delete_required_path(self, mockobj):
        """
        Test that required paths on delete raise error
        """
        obj, _ = mockobj

        with pytest.raises(ImproperlyConfigured):
            # Path is required on access
            path = obj.standard_path

        # Set to a file, and we're good to go
        obj.standard_path = TESTFILE
        path = obj.standard_path
        assert path == TESTFILE

        # Now try to delete it
        del obj.standard_path
        with pytest.raises(ImproperlyConfigured):
            path = obj.standard_path

    def test_default_path(self, mockobj):
        """
        Check that a default path is returned when not set
        """
        obj, _ = mockobj

        # Make sure the default is available
        assert obj.default_path is not None
        assert obj.default_path == TESTDIR

        # Change the default to the test file
        obj.default_path = TESTFILE
        assert obj.default_path == TESTFILE

        # Now delete the test file and check default again
        del obj.default_path
        assert obj.default_path is not None
        assert obj.default_path == TESTDIR

    def test_required_path(self, mockobj):
        """
        Assert that paths are required
        """
        obj, _ = mockobj
        with pytest.raises(ImproperlyConfigured):
            obj.standard_path

    def test_not_required_path(self, mockobj):
        """
        Assert not required paths don't raise an error
        """
        obj, _ = mockobj

        try:
            path = obj.not_required_path
            assert path is None
        except ImproperlyConfigured:
            pytest.fail("a non-required path raised a configuration error")

    def test_path_not_found_warning(self, mockobj):
        """
        Test that PathNotFound is warned on not raises
        """
        obj, _ = mockobj

        with pytest.warns(PathNotFound):
            assert not MockObject.dont_raise_path.mkdirs
            assert not os.path.exists(MISSDIR)

            # Trigger a warning.
            obj.dont_raise_path = MISSDIR

    @pytest.mark.filterwarnings("ignore")
    def test_user_expansion(self, mockobj):
        """
        Test that on set, user is expanded.
        """
        obj, _ = mockobj

        testpath = "~/path/to/test"
        obj.dont_raise_path = "~/path/to/test"
        assert obj.dont_raise_path == os.path.expanduser(testpath)

    @pytest.mark.filterwarnings("ignore")
    def test_vars_expansion(self, mockobj):
        """
        Test that on set, vars are expanded.
        """
        obj, _ = mockobj
        obj.standard_path = "${}".format(ENVVAR)
        assert obj.standard_path == VARSDIR

    @pytest.mark.filterwarnings("ignore")
    def test_normpath_path(self, mockobj):
        """
        Test that on set the path is normed
        """
        obj, _ = mockobj

        # Use the not raises so that we don't have to create the user path
        path = os.path.join(VARSDIR, "..")
        obj.standard_path = path
        assert obj.standard_path == TEMPDIR

    @pytest.mark.filterwarnings("ignore")
    def test_absolute_path(self, mockobj):
        """
        Test that the path is transformed into an absolute path
        """
        obj, _ = mockobj

        # Use the not raises so that we don't have to create the user path
        relative_path = "path/to/test.txt"
        obj.dont_raise_path = relative_path
        assert obj.dont_raise_path == os.path.abspath(relative_path)

    @pytest.mark.filterwarnings("ignore")
    def test_not_absolute_path(self, mockobj):
        """
        Test that the path is not transformed into an absolute path
        """
        obj, _ = mockobj
        # Use the not raises so that we don't have to create the user path
        relative_path = "path/to/test.txt"
        obj.not_absolute = relative_path
        assert obj.not_absolute == relative_path

    def test_mkdirs_path(self, mockobj):
        """
        Test that a directory is created on mkdirs = True
        """
        obj, _ = mockobj
        assert not os.path.exists(MISSDIR)
        obj.mkdirs_path = MISSDIR
        assert os.path.exists(MISSDIR)

    @pytest.mark.filterwarnings("ignore")
    def test_no_mkdirs_path(self, mockobj):
        """
        Test that no directory is created by default
        """
        obj, _ = mockobj

        assert not os.path.exists(MISSDIR)
        obj.silent_path = MISSDIR
        assert not os.path.exists(MISSDIR)

    def test_raises_path(self, mockobj):
        """
        Test that if raises is True, an exception happens
        """
        obj, _ = mockobj
        for path in ('standard_path', 'default_path', 'not_required_path'):
            with pytest.raises(ImproperlyConfigured):
                assert not os.path.exists(MISSDIR)
                setattr(obj, path, MISSDIR)

    @pytest.mark.filterwarnings("ignore")
    def test_not_raises_path(self, mockobj):
        """
        Assert other paths don't raise an exception
        """
        obj, _ = mockobj
        for path in ('mk_no_raise_path', 'dont_raise_path', 'not_absolute', 'silent_path'):
            try:
                if os.path.exists(MISSDIR):
                    shutil.rmtree(MISSDIR)

                setattr(obj, path, MISSDIR)
            except ImproperlyConfigured:
                self.fail("Improperly configured raised on %s" % path)
