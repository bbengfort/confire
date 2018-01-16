# Confire
[![Build Status][build_status_img]][build_status_page]
[![Coverage Status][coveralls_img]][coveralls_page]
[![PyPi version][pypi_version_img]][pypi_version]
[![PyPi downloads][pypi_downloads_img]][pypi_downloads]
[![Stories in Ready][waffle_img]][waffle_status]
[![Documentation Status][rtd_img]][rtd_page]

**A simple app configuration scheme using YAML and class based defaults.**

[![Confire][confire.jpg]][confire.jpg]

Confire is a simple but powerful configuration scheme that builds on the configuration parsers of Scapy, elasticsearch, Django and others. The basic scheme is to have a configuration search path that looks for YAML files in standard locations. The search path is hierarchical (meaning that system configurations are overloaded by user configurations, etc). These YAML files are then added to a default, class-based configuration management scheme that allows for easy development.

Full documentation can be found here: [http://confire.readthedocs.org/](http://confire.readthedocs.org/)

## Features

* Configuration files in YAML
* Hierarchical configuration search
* Class based application defaults
* Settings pulled in from the environment

## Example Usage

Create a file called "myapp.yaml" and place it in one of the following places:

* /etc/myapp.yaml
* $HOME/.myapp.yaml
* conf/myapp.yaml

Create some configuration values inside the file like so:

```yaml
## Set application environment
debug:   True
testing: False

## A simple database configuration
database:
    name: mydb
    host: localhost
    port: 5432
    user: postgres
```

In your code, create a file called "config.py" and add the following:

```python
import os
from confire import Configuration
from confire import environ_setting

class DatabaseConfiguration(Configuration):

    host = "localhost"
    port = 5432
    name = "mydb"
    user = "postgres"
    password = environ_setting("DATABASE_PASSWORD", required=False)

class MyAppConfiguration(Configuration):

    CONF_PATHS = [
        '/etc/myapp.yaml',
        os.path.expanduser('~/.myapp.yaml'),
        os.path.abspath('conf/myapp.yaml')
    ]

    debug    = False
    testing  = True
    database = DatabaseConfiguration()


settings = MyAppConfiguration.load()
```

Now, everywhere in your code that you would like to access these settings values, simply use as follows:

```python
from config import settings

debug = settings.get('DEBUG') or settings['DEBUG']
```

Voila! A complete configuration system for your application!

### A note on environment variables

Confire is setup to enable the use of environment variables, especially if you use the helper `environ_setting` method that comes with Confire. Just note, however, that a settings file will always override the Environment, not the other way around! Sensitive values should never be placed in a settings file anyway, but rather added to the environment at run time.

The `environ_setting` alows you to specify required or optional settings to fetch from the ENVIRONMENT as defaults. It also allows you to specify a default if the ENVVAR is not there. See the documentation for more details.

## Setup

The easiest and usual way to install confire is to use pip:

```bash
~$ pip install confire
```

To install the package from source, download the latests package tarball, unzip in a temporary directory and run the following command:

```bash
~$ python setup.py install
```

As always, I highly recommend the use of a virtual environment to better manage the software dependencies for your particular code base.

## About

There are many configuration packages available on PyPI - it seems that everyone has a different way of doing it. However, this is my prefered way, and I found that after I copy and pasted this code into more than 3 projects that it was time to add it as a dependency via PyPI. The configuration builds on what I've learned/done in configuring Scapy, elasticsearch, and Django - and builds on these principles:

1. Configuration _should not_ be Python (sorry Django). It's too easy to screw stuff up, and anyway, you don't want to deal with importing a settings file from /etc!
2. Configuration should be on a per-system basis. This means that there should be an /etc/app.yaml configuration file as well as a $HOME/.app.yaml configuration file that overwrites the system defaults for a particular user. For development purposes there should also be a $(pwd)/app.yaml file so that you don't have to sprinkle things throughout the system if not needed.
3. Developers should be able to have reasonable defaults already written in code if no YAML file has been provided. These defaults should be added in an API like way that is class based and modularized.
4. Accessing settings from the code should be easy.

So there you have it, with these things in mind I wrote confire and I hope you enjoy it!

### Name Origin

<big>con &middot; fit</big><br />
/kôNˈfē/<br/>
*noun* duck or other meat cooked slowly in its own fat.

Origin<br />
[French] *confire*: to prepare<br />
Also refers to the culinary art of pickling

I like cooking, and the thought of preparation in French culinary language appealed to me. The way I got here was to simply change the "g" in config to a "t". A definition lookup and boom, a name!

## Contributing

Confire is open source, and I would be happy to have you contribute! You can contribute in the following ways:

1. Create a pull request in Github: [https://github.com/bbengfort/confire](https://github.com/bbengfort/confire)
2. Add issues or bugs on the bugtracker: [https://github.com/bbengfort/confire/issues](https://github.com/bbengfort/confire/issues)
3. Checkout the current dev board on waffle.io: [https://waffle.io/bbengfort/confire](https://waffle.io/bbengfort/confire)

You can contact me on Twitter if needed: [@bbengfort](https://twitter.com/bbengfort)


### Development

Development on this project is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Fork and clone the confire library into your own Github account

2. Select a card from the [waffle dev board](https://waffle.io/bbengfort/confire) - preferably one that is "ready" then move it to "in-progress".

3. Checkout the develop branch to begin development

        $ git fetch
        $ git checkout develop

4. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        $ git checkout -b feature-myfeature develop

5. Once you are done working (and everything is tested) merge your feature into develop.

        $ git checkout develop
        $ git merge --no-ff feature-myfeature
        $ git branch -d feature-myfeature
        $ git push origin develop

6. Repeat steps 4-5 until you are ready to submit your changes. Readiness should include tests that work (pull requests will require Travis tests to pass), as well as some documentation.

7. Submit a pull request back to the main confire library, to the develop branch.

8. Releases will be routinely pushed into master via release branches, then deployed to PyPi - the master branch should reflect the latest release.

## Changelog

The release versions that are sent to the Python package index are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of confire.

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bugfixes or other micro changes that developers should feel free to immediately update to.

### v0.2.1 pending release ###

* **tag**: v0.2.1
* **deployment**: pending
* **commit**: (latest)

So far this release has done some package maintenance, for example using a version methodology that I've written about at District Data Labs. Confire continues to work and perform with the latest releases of Python and the PyYAML dependency, so only minor bugfixes will be in this release.

### v0.2.0 released on 31 July 2014 ###

* **tag**: v0.2.0
* **deployment**: July 31, 2014
* **commit**: 9167120

This release will add some new features including support for environmental variables as settings defaults, ConfigurationMissing Warnings and ImproperlyConfigured errors that you can raise in your own code to warn developers about the state of configuration.

This release also greatly increased the amount of available documentation for Confire.

### v0.1.1 released on 24 July 2014 ###

* **tag**: v0.1.1
* **deployment**: July 24, 2014
* **commit**: bdc0488

Added Python 3.3 support thanks to [@tyrannosaurus](https://github.com/tyrannosaurus) who contributed to the changes that would ensure this support for the future. I also added Python 3.3 travis testing and some other minor changes.

### v0.1.0 released on 20 July 2014 ###

* **tag**: v0.1.0
* **deployment**: July 20, 2014
* **comit**: 213aa5e

Initial deployment of the confire library.

<!-- References -->
[build_status_img]: https://travis-ci.org/bbengfort/confire.svg?branch=master
[build_status_page]: https://travis-ci.org/bbengfort/confire
[coveralls_img]: https://coveralls.io/repos/bbengfort/confire/badge.svg?branch=master
[coveralls_page]: https://coveralls.io/r/bbengfort/confire?branch=master
[rtd_img]: https://readthedocs.org/projects/confire/badge/?version=latest
[rtd_page]: https://readthedocs.org/projects/confire/?badge=latest
[confire.jpg]: http://upload.wikimedia.org/wikipedia/commons/d/d4/Picholines_et_Olives_Nyons.jpg
[pypi_version]: http://badge.fury.io/py/confire
[pypi_version_img]: https://badge.fury.io/py/confire.svg
[pypi_downloads]: https://pypi.python.org/pypi/confire/0.2.0
[pypi_downloads_img]: https://img.shields.io/pypi/dm/confire.svg
[waffle_img]: https://badge.waffle.io/bbengfort/confire.png?label=ready&title=Ready
[waffle_status]: https://waffle.io/bbengfort/confire
