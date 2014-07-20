.. Confire documentation master file, created by
   sphinx-quickstart on Sun Jul 20 13:23:44 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Confire
=======

Confire is a simple but powerful configuration scheme that builds on the configuration parsers of Scapy, elasticsearch, Django and others. The basic scheme is to have a configuration search path that looks for YAML files in standard locations. The search path is hierarchical (meaning that system configurations are overloaded by user configurations, etc). These YAML files are then added to a default, class-based configuration management scheme that allows for easy development.

Features
--------

- Configuration files in YAML
- Hierarchical configuration search
- Class based application defaults
- Settings pulled in from the environment

Example Usage
-------------

Create a file called "myapp.yaml" and place it in one of the following places:

- ``/etc/myapp.yaml``
- ``$HOME/.myapp.yaml``
- ``conf/myapp.yaml``

Create some configuration values inside the file like so:

.. code-block :: yaml

   ## Set application environment
   debug:   True
   testing: False

   ## A simple database configuration
   database:
       name: mydb
       host: localhost
       port: 5432
       user: postgres

In your code, create a file called "config.py" and add the following:

.. code-block :: python

   import os
   from confire import Configuration

   class DatabaseConfiguration(Configuration):

       host = "localhost"
       port = 5432
       name = "mydb"
       user = "postgres"
       password = os.environ.get("DATABASE_PASSWORD", "")

   class MyAppConfiguration(Configuration):

       CONF_PATHS = [
           '/etc/myapp.yaml',
           os.path.expanduser('~/.myapp.yaml')
           os.path.abspath('conf/myapp.yaml)
       ]

       debug    = False
       testing  = True
       database = DatabaseConfiguration()

   settings = MyAppConfiguration.load()

Now, everywhere in your code that you would like to access these settings values, simply use as follows:

.. code-block :: python

   from config import settings

   debug = settings.get('DEBUG') or settings['DEBUG']

Voila! A complete configuration system for your application!

Setup
-----

The easiest and usual way to install confire is to use pip:

.. code-block :: bash

   pip install confire

To install the package from source, download the latests package tarball, unzip in a temporary directory and run the following command:

.. code-block :: bash

   python setup.py install

As always, I highly recommend the use of a virtual environment to better manage the software dependencies for your particular code base.

About
-----

There are many configuration packages available on PyPI - it seems that everyone has a different way of doing it. However, this is my prefered way, and I found that after I copy and pasted this code into more than 3 projects that it was time to add it as a dependency via PyPI. The configuration builds on what I've learned/done in configuring Scapy, elasticsearch, and Django - and builds on these principles:

1. Configuration *should not* be Python (sorry Django). It's too easy to screw stuff up, and anyway, you don't want to deal with importing a settings file from ``/etc``!
2. Configuration should be on a per-system basis. This means that there should be an ``/etc/app.yaml`` configuration file as well as a ``$HOME/.app.yaml`` configuration file that overwrites the system defaults for a particular user. For development purposes there should also be a ``$(pwd)/app.yaml`` file so that you don't have to sprinkle things throughout the system if not needed.
3. Developers should be able to have reasonable defaults already written in code if no YAML file has been provided. These defaults should be added in an API like way that is class based and modularized.
4. Accessing settings from the code should be easy.

So there you have it, with these things in mind I wrote confire and I hope you enjoy it!

Contributing
~~~~~~~~~~~~

Confire is open source, and I would be happy to have you contribute! You can contribute in the following ways:

1. Create a pull request in Github: https://github.com/bbengfort/confire
2. Add issues or bugs on the bugtracker: https://github.com/bbengfort/confire/issues
3. Checkout the current dev board on waffle.io: https://waffle.io/bbengfort/confire

You can contact me on Twitter if needed: `@bbengfort`_

.. _@bbengfort: (https://twitter.com/bbengfort)

Name Origin
~~~~~~~~~~~
.. raw :: html

    con &middot; fit<br />
    /kôNˈfē/<br/>
    <em>noun</em> duck or other meat cooked slowly in its own fat.<br /><br />

    Origin<br />
    [French] <em>confire</em>: to prepare<br \>
    Also refers to the culinary art of pickling

I like cooking, and the thought of preparation in French culinary language appealed to me. The way I got here was to simply change the "g" in config to a "t". A definition lookup and boom, a name!

Changelog
---------

The release versions that are sent to the Python package index are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of confire.

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bugfixes or other micro changes that developers should feel free to immediately update to.

v0.1.0 released on 20 July 2014
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **tag**: v0.1.0
* **deployment**: July 20, 2014
* **comit**: --

Initial deployment of the confire library.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

