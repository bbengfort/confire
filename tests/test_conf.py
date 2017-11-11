# tests.test_conf
# Testing the configuration module for Confire
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 20 09:43:33 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: test_conf.py [] benjamin@bengfort.com $

"""
Testing the configuration module for Confire

TODO: Write test for None values in config
TODO: Ensure that "empty" values e.g. [], and {} override on config
TODO: Ensure that configure method is working correctly
TODO: Ensure that testing is not dependent on a user's configuration
"""

##########################################################################
## Imports
##########################################################################

import os
import shutil
import pytest

from copy import copy
from confire.config import *
from confire.exceptions import *


##########################################################################
## Fixtures
##########################################################################

os.environ['TESTING_CONFIRE_PASSWORD'] = 'supersecretsquirrel'
TESTDATA = os.path.join(os.path.dirname(__file__), "testdata")
TESTCONF = os.path.join(TESTDATA, "testconf.yaml")


class SubNestedConfiguration(Configuration):

    level = 2


class NestedConfiguration(Configuration):

    level  = 1
    empty  = []
    nested_path = path_setting(raises=False, required=False)
    nested = SubNestedConfiguration()


class MockConfiguration(Configuration):
    """
    A subclass of the Configuration class for testing purposes.
    """

    _notanopt = "joe"
    NOTANOPT  = "bob"
    mysetting = True
    anoption  = 42
    paththere = "/var/log/there.pth"
    nested    = NestedConfiguration()
    password  = environ_setting('TESTING_CONFIRE_PASSWORD')
    myfile    = path_setting(raises=False)
    datadir   = path_setting(default='/tmp/data/', raises=False)

    def amethod(self):
        return True


@pytest.fixture(scope='function')
def emptyconfig():
    """
    Remove default config paths to ensure clean tests
    """
    original_conf_paths = copy(Configuration.CONF_PATHS)
    Configuration.CONF_PATHS = []
    yield original_conf_paths
    Configuration.CONF_PATHS = original_conf_paths


@pytest.fixture(scope='function')
def testconfig(tmpdir, emptyconfig):
    """
    Copy the testconf.yaml file to a temporary directory and modify the
    lookup path of the Configuration object to look for it.
    """
    f = tmpdir.mkdir("conf").join("test.yaml")
    path = str(f)
    shutil.copy2(TESTCONF, path)
    Configuration.CONF_PATHS = [path]
    yield path
    f.remove()


##########################################################################
## Configuration Unit Tests
##########################################################################

class TestConfig(object):

    def test_search_path(self):
        """
        Assert there are default directories to search for configuration
        """
        assert len(Configuration.CONF_PATHS) > 0

    def test_empty_conf_path(self, emptyconfig):
        """
        Test that an empty conf path raises no exceptions
        """
        config = MockConfiguration.load()
        assert len(Configuration.CONF_PATHS) == 0
        assert config['mysetting']
        assert config.get('myprop') is None

    @pytest.mark.filterwarnings("ignore")
    def test_load_config(self, testconfig):
        """
        Assert config can load from YAML
        """

        config = MockConfiguration.load()

        assert config.get('myfile') is not None
        assert config.get('myprop') is not None
        assert isinstance(config.get('nested'), NestedConfiguration)
        assert config.get("nested").get("level") == "floor"

    @pytest.mark.filterwarnings("ignore")
    def test_load_override(self, testconfig):
        """
        Assert that loading config overrides default
        """
        config = MockConfiguration.load()
        assert not config["mysetting"]

    def test_configure_by_dict(self):
        """
        Check configuration by dictionary
        """
        config = MockConfiguration.load()
        config.configure({"anoption":45, "foo":"bar"})
        assert config["anoption"] == 45
        assert config["foo"] == "bar"

    @pytest.mark.filterwarnings("ignore")
    def test_configure_by_conf(self):
        """
        Check configuration by other configuration
        """

        configa = MockConfiguration.load()
        configb = MockConfiguration.load()

        assert configa["anoption"] == configb["anoption"]

        configa.anoption = 80
        assert configa["anoption"] != configb["anoption"]

        configb.configure(configa)
        assert configa["anoption"] == configb["anoption"]

    @pytest.mark.filterwarnings("ignore")
    def test_configure_with_none(self):
        """
        Ensure None passed to configure doesn't break
        """
        config = MockConfiguration.load()
        try:
            config.configure(None)
        except Exception:
            pytest.fail("None passed to configure raised an error!")

    @pytest.mark.filterwarnings("ignore")
    def test_nested_configure(self):
        """
        Ensure nested configurations work
        """
        config = MockConfiguration.load()
        data   = {"nested": {"nested": {"level":"basement"}, "level": "lobby"}}
        config.configure(data)
        assert isinstance(config.get('nested'), NestedConfiguration)
        assert isinstance(config.get('nested').get('nested'), SubNestedConfiguration)
        assert config.get('nested').get('level') == 'lobby'
        assert config.get('nested').get('nested').get('level') == 'basement'

    @pytest.mark.filterwarnings("ignore")
    def test_environ_configuration(self):
        """
        Test the environ setting on a config
        """
        config = MockConfiguration.load()
        assert config.get('password') == 'supersecretsquirrel'

    @pytest.mark.filterwarnings("ignore")
    def test_settings_file_environ_override(self, testconfig):
        """
        Test that the settings file overrides the environ
        """
        config = MockConfiguration.load()
        assert config.get('password') == 'knockknock'

    def test_path_configuration(self, tmpdir):
        """
        Test the path setting on a config
        """
        config = MockConfiguration.load()
        with pytest.raises(ImproperlyConfigured):
            config.myfile

        assert config.datadir == '/tmp/data/'

    @pytest.mark.filterwarnings("ignore")
    def test_settings_file_path_configuration(self, testconfig):
        """
        Test the paths loaded from the settings file
        """
        config = MockConfiguration.load()
        assert os.path.expanduser('~/tmp/data.txt') == config.myfile
        assert '/tmp/data/' == config.datadir

    @pytest.mark.filterwarnings("ignore")
    def test_nested_path(self, testconfig):
        """
        Tested nested path configuration
        """
        config = MockConfiguration.load()
        assert config.nested.nested_path == '/tmp'
        assert config['nested']['nested_path'] == '/tmp'
        assert config['NESTED']['NESTED_PATH'] == '/tmp'

    def test_options(self):
        """
        Test the options method
        """
        config = MockConfiguration.load()
        options = dict(config.options())

        assert "mysetting" in options
        assert "anoption" in options
        assert "paththere" in options

        assert "_notanopt" not in options
        assert "amethod" not in options
        assert "NOTANOPT" not in options

    def test_get(self):
        """
        Assert that get returns default or key
        """
        config = MockConfiguration.load()
        assert config.get("mysetting")
        assert "notanopt" not in dict(config.options())
        assert config.get("notanopt", 1) == 1

    def test__get__(self):
        """
        Check the getkey method
        """
        config = MockConfiguration.load()
        assert config["mysetting"]

    def test_case_insensitivity(self):
        """
        Assert case insensitivity in getitem
        """
        config = MockConfiguration.load()
        assert config["MYSETTING"]

    def test_key_error(self):
        """
        Assert not found key raises an exception
        """
        with pytest.raises(KeyError):
            config = MockConfiguration.load()
            assert config["notanopt"]

    @pytest.mark.filterwarnings("ignore")
    def test_configure_back_to_empty(self, testconfig):
        """
        Can override an empty list or dictionary from configuration
        """
        # Setup normal configuration
        config = MockConfiguration.load()
        assert len(config.nested.empty) > 0, "configuration was not loaded"

        # Now reoverride with original settings - like the TestingConfig
        config.nested.configure(NestedConfiguration())
        assert len(config.nested.empty) == 0
        assert config.nested.level == 1
