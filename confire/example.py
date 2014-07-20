# confire.example
# This is an example configuration file
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 20 14:56:39 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: example.py [] benjamin@bengfort.com $

"""
This file is an example file that you might put into your code base to
have a configuration library at your fingertips!
"""

##########################################################################
## Imports
##########################################################################

import os
from confire import Configuration

##########################################################################
## Database Configuration
##########################################################################

class DatabaseConfiguration(Configuration):
    """
    This object contains the default connections to a Postgres Database.
    """

    host            = "localhost"
    port            = 5432
    database        = "app"
    user            = "postgres"
    password        = os.environ.get("DATABASE_PASSWORD")

##########################################################################
## Confire Configuration Defaults
##########################################################################

class ExampleConfiguration(Configuration):
    """
    This object contains an example configuration.

    debug: allow debug checking
    testing: are we in testing mode?
    """

    CONF_PATHS = [
        '/etc/myapp.yaml',                    # The global configuration
        os.path.expanduser('~/.myapp.yaml'),  # User specific configuration
        os.path.abspath('conf/myapp.yaml'),   # Local directory configuration
        os.path.abspath('conf/example-config.yaml')
    ]

    debug           = True
    testing         = False
    database        = DatabaseConfiguration()

##########################################################################
## Import this loaded Configuration
##########################################################################

settings = ExampleConfiguration.load()

if __name__ == '__main__':
    print settings
