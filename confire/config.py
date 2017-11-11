# confire.conf
# A simple configuration module for Confire
#
# Author:   Benjamin Bengfort <ben@cobrain.com>
# Created:  Tue May 20 22:19:11 2014 -0400
#
# Copyright (C) 2013 Cobrain Company
# For license information, see LICENSE.txt
#
# ID: conf.py [] ben@cobrain.com $

"""
Confire class for specifying Confire specific optional items via a YAML
configuration file format. The main configuration class provides utilities
for loading the configuration from disk and iterating across all the
settings. Subclasses of the Configuration specify defaults that can be
updated via the configuration files.

General usage:

    from confire.conf import settings
    mysetting = settings.get('mysetting', default)

You can also get settings via a dictionary like access:

    mysetting = settings['mysetting']

However, this will raise an exception if the setting is not found.

Note: Keys are CASE insensitive

Note: Settings can be modified directly by settings.mysetting = newsetting
however, this is not recommended, and settings should be fetched via the
dictionary-like access.
"""

##########################################################################
## Imports
##########################################################################

import os
import yaml
import warnings

from six import with_metaclass

from .paths import Path
from .descriptors import SettingsMeta
from .exceptions import ImproperlyConfigured, ConfigurationMissing

##########################################################################
## Environment helper function
##########################################################################

def environ_setting(name, default=None, required=True):
    """
    Fetch setting from the environment. The bahavior of the setting if it
    is not in environment is as follows:

        1. If it is required and the default is None, raise Exception
        2. If it is requried and a default exists, return default
        3. If it is not required and default is None, return  None
        4. If it is not required and default exists, return default
    """
    if name not in os.environ and default is None:
        message = "The {0} ENVVAR is not set.".format(name)
        if required:
            raise ImproperlyConfigured(message)
        else:
            warnings.warn(ConfigurationMissing(message))

    return os.environ.get(name, default)

##########################################################################
## Paths helper function
##########################################################################

def path_setting(**kwargs):
    """
    Helper function to enable the configuration of paths on the local file
    system. By default, this function manages strings in the YAML file:

        1. Expand user (e.g. ~)
        2. Expand vars (e.g. $HOME)
        3. Normalize the path (e.g. .. and . resolution)
        4. If absolute, return the absolute path

    If mkdirs is True, then this function will create the directory if it
    does not exist. If raises is True, then it will raise an exception if the
    directory does not exist.
    """
    return Path(**kwargs)

##########################################################################
## Configuration Base Class
##########################################################################

class Configuration(with_metaclass(SettingsMeta, object)):
    """
    Base configuration class specifies how configurations should be
    handled and provides helper methods for iterating through options and
    configuring the base class.

    Subclasses should provide defaults for the various configurations as
    directly set class level properties. Note, however, that ANY directive
    set in a configuration file (whether or not it has a default) will be
    added to the configuration.

    Example:

        class MyConfig(Configuration):

            mysetting = True
            logpath   = "/var/log/myapp.log"
            appname   = "MyApp"

    The configuration is then loaded via the classmethod `load`:

        settings = MyConfig.load()

    Access to properties is done two ways:

        settings['mysetting']
        settings.get('mysetting', True)

    Note: None settings are not allowed!
    """

    CONF_PATHS = [
        '/etc/confire.yaml',                    # The global configuration
        os.path.expanduser('~/.confire.yaml'),  # User specific configuration
        os.path.abspath('conf/confire.yaml')    # Local directory configuration
    ]

    @classmethod
    def load(klass):
        """
        Insantiates the configuration by attempting to load the
        configuration from YAML files specified by the CONF_PATH module
        variable. This should be the main entry point for configuration.
        """
        config = klass()
        for path in klass.CONF_PATHS:
            if os.path.exists(path):
                with open(path, 'r') as conf:
                    config.configure(yaml.safe_load(conf))
        return config

    def configure(self, conf={}):
        """
        Allows updating of the configuration via a dictionary of
        configuration terms or a configuration object. Generally speaking,
        this method is utilized to configure the object from a JSON or
        YAML parsing.
        """
        if not conf: return
        if isinstance(conf, Configuration):
            conf = dict(conf.options())
        for key, value in conf.items():
            opt = self.get(key, None)
            if isinstance(opt, Configuration):
                opt.configure(value)
            else:
                setattr(self, key, value)

    def options(self):
        """
        Returns an iterable of sorted option names in order to loop
        through all the configuration directives specified in the class.
        """
        keys = self.__class__.__dict__.copy()
        keys.update(self.__dict__)
        keys = sorted(keys.keys())

        for opt in keys:
            val = self.get(opt)
            if val is not None:
                yield opt, val

    def get(self, key, default=None):
        """
        Fetches a key from the configuration without raising a KeyError
        exception if the key doesn't exist in the config or
        ImproperlyConfigured if the key doesn't exist, instead it returns the
        default (None).
        """
        try:
            return self[key]
        except (KeyError, ImproperlyConfigured):
            return default

    def __getitem__(self, key):
        """
        Main configuration access method. Performs a case insensitive
        lookup of the key on the class, filtering methods and pseudo
        private properties. Raises KeyError if not found. Note, this makes
        all properties that are uppercase invisible to the options.
        """
        key = key.lower()
        if hasattr(self, key):
            attr = getattr(self, key)
            if not callable(attr) and not key.startswith('_'):
                return attr
        raise KeyError(
            "{} has no configuration '{}'".format(
            self.__class__.__name__, key
        ))

    def __repr__(self):
        return str(self)

    def __str__(self):
        s = ""
        for opt, val in self.options():
            r = repr(val)
            r = " ".join(r.split())
            wlen = 76-max(len(opt),10)
            if len(r) > wlen:
                r = r[:wlen-3]+"..."
            s += "%-10s = %s\n" % (opt, r)
        return s[:-1]
