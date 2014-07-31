.. Confire documentation file, created by Benjamin Bengfort on Thu Jul 31 12:01:34 2014.

Configuring Apps with Confire
=============================

Let's say that you've just started a new Python project - you know that
this project is going to need access to a Database, possibly require an
API key and API Secret, and it will definitely need some sort of debug mode
so that developers can figure out what's going on in production. These
types of variables shouldn't be hardcoded into your application, you'll
want some kind of configuration management system in your app.

So what are your options? Python has a native configuration parser that
handles .ini files similar to what you'd see on Windows machines - it's
called ``configparser``, and while it works well (and even has support for
JSON files) - it is extremely basic. As a developer, you not only have to
deal with the .ini syntax, but you also have to look for the file and load
it into the parser. While the parser does handle type conversion, it has
no quick ability to add reasonable defaults. Basically, your configuration
ends up being defined by the .ini file - and this is not good, especially
if your users forget to change a particular value or leave one out all
together!

If you look at Django, they have their settings in a Python file, and the
settings are Python code. This is great because now you can use any Python
type as a setting. There are even reasonable defaults and some fancy import
logic helps get the settings where they need to be. The problem is that
you have to import that file, it has to be on your python path - so no
storage of a settings file in /etc or any other reasonable place. It also
means that *developers* have to configure Django- not just users of the
app.

So we want the following things in our configuration:

#. Reasonable lookup locations for config files
#. Configuration type parsing from a text file
#. An API that supports reasonable defaults and in-code usage
#. A text based configuration that is for users not developers

This is where confire comes in. Confire uses YAML as the configuration
language of choice. This is a markup format that has rich types like JSON,
but is also very readable. Applications like Elasticsearch, Ruby on Rails,
Travis-CI and others make use of YAML, so it's probably already familiar
to you.

Confire has a hierarchical lookup system that means it looks in the system
configuration (``/etc`` in *nix systems), then in a user specific place,
then in a local directory. At each level, the configuration overrides the
defaults from the other levels. Configurations are then supplied to the
developer in a friendly, Django-like way.

Project Setup
-------------

In your projects folder, create your app folder, let's call it "myapp".
Then create the Python project skeleton as you would normally do, but also
include a configuration directory, "conf".

.. code-block :: bash

    $ mkdir myapp
    $ cd myapp
    $ mkdirs bin tests conf docs fixtures myapp
    $ touch tests/__init__.py
    $ touch myapp/__init__.py
    $ touch setup.py
    $ cd docs
    $ sphinx-quickstart
    ...
    $ cd ..

Hopefull this is very familiar to those who develop on Linux or Mac and
set up Python projects regularly. Now, assuming you're using Git as well
as virtualenv and virtualenv wrapper - let's get our repository and env
going:

.. code-block :: bash

    $ git init
    $ mkvirtualenv -a $(pwd) myapp
    (myapp)$ pip install confire
    (myapp)$ pip install nose
    (myapp)$ pip freeze > requirements.txt

Perfect! You're now ready to get developing your Python app. Let's start
by getting our configuration going. Create a file called ``myapp.yaml`` in
the ``conf`` directory. It may be helpful to add this file to your
``.gitignore`` so that you don't accidentally commit a private variable
publically. Also create a file called ``config.py`` in your ``myapp``
module.

Inside the ``myapp.yaml`` file place the following, very simple code.

.. code-block :: yaml

    debug: false
    testing: false

And then inside your ``config.py``, place the following code.

.. code-block :: python

    import os
    from confire import Configuration

    class MyAppConfiguration(Configuration):

        CONF_PATHS = [
            "/etc/myapp.yaml",                          # System configuration
            os.path.expandvars("$HOME/.myapp.yaml"),    # User specific configuration
            os.path.abspath("conf/myapp.yaml"),         # Development configuration
        ]

        debug   = True
        testing = True

    ## Load settings immediately for import
    settings = MyAppConfiguration.load()

    if __name__ == "__main__":
        print settings

That's it, you now have a complete configuration system for your app! Let's
walk through this code. Confire provides a class-based configuration API,
meaning that you simply create configuration classes and then defeine your
defaults on them at the class level (kind of like you might use Django
class-based views). Configuration classes must all extend the
``confire.Configuration`` base class.

.. note :: All configurations should be lowercase properties!
    Configurations are case insensitive, but to achieve this,
    the ``__getitem__`` method lowercases all accessors!

The ``CONF_PATHS`` class variable tells the configuration where to look
for YAML files to load. In this case, we specify three lookups that happen
in the order they're specified - first the system, then the user directory,
then the local directory for development. You'll notice that if the config
file is missing, no exceptions are raised.

Using Configurations in Code
----------------------------

The loaded settings immediately for import means that elsewhere in your
code, all you have to do is use the following to get access to your config:

.. code-block :: python

    from myapp.config import settings

    if settings.get("DEBUG"):
        ...
    else:
        ...

Because your API has already specified reasonable defaults, you don't have
to worry about configurations being missing or unavailable!

A couple notes on using the settings in your code:

#. The settings *are not* case sensitive, DEBUG is the same as debug.
   However, all properties should be stored as lowercase in the
   configuration subclass.
#. You can access settings like so: ``settings["mysetting"]``, however this
   will raise an exception if the setting is not available (something that
   really shouldn't happen).
#. You can also access the settings through the get method:
   ``settings.get("mysetting", "foo")``, which will not raise an exception
   on a missing setting, but instead return the supplied default or ``None``.
#. You can also access the settings using a dot accessor method:
   ``settings.mysetting``, which fetches the properties off the class.
#. Settings can be modified at runtime, but this is not recommended.

As you continue to develop, you can add settings to your ``config.py`` as
well as your ``myapp.yaml``, your app development is now much smoother!

Environment Variables
=====================

Sometimes you don't want your configurations to reside inside of a YAML
file, saved on disk, usually when you have a secret key or a database
password. Other times you don't have access to your server's disk, but
can add ENVIRONMENTAL VARIABLES as with a hosting service like Heroku.

Confire makes it easy to specify variables that you expect to be in the
environment, using the ``environ_setting`` function, which you can import
from the main module.

.. code-block :: python

    from confire import Configuration, environ_setting

    class MyConfiguration(Configuration):

        supersecret = environ_setting("SUPER_SECRET", None, required=True)

The function expects as a first argument, the name of the environment
variable, usually an all caps, underscore separated name. You can also
give a default value (in case no variable exists in the environment) as
the second argument.

When the environment is initialized (not loaded) it will immediately look
in the environment for the setting and store it as the default. Any
settings that are in the YAML search paths will override the environment
variable, so make sure that you leave ENV_VARS out of the YAML configs!

The behavior of the function depends on how it's called, in terms of using
the default and fetching from the environment:

#. If it is required and the default is None, raise ImproperlyConfigured
#. If it is requried and a default exists, return default
#. If it is not required and default is None, return  None
#. If it is not required and default exists, return default

Environmental variables are usually required, hence the exception.

Note also that you can use confire exceptions and warnings in your own
code, by importing the ``ImproperlyConfigured`` and ``MissingConfiguration``
exception and warning.

Nested Configurations
=====================

Configurations are nestable in order to ensure that developers can create
easily modular configurations, for example database configuations for a
staging and production database or per-app settings. Nested configurations
will also be loaded from a single YAML file that expects a similar nesting
structure, and the configurations are loaded in a depth-first manner.

To create a nested configuration, you need a main configuration object
that supports the top-level configuration. For each nested configuration,
you simply create new ``Configuration`` subclasses and then add them as
settings to main configuration class.

Here is the example for two different databases:

.. code-block :: python

    import confire

    class DatabaseConfiguration(confire.Configuration):

        name   = None
        host   = "localhost"
        port   = 5432
        user   = None
        pass   = None

    class MainConfiguration(confire.Configuration):

        staging    = DatabaseConfiguration()
        production = DatabaseConfiguration()

    settings = MainConfiguration.load()

In your YAML file, you can configure each database configuration for its
specific environment:

.. code-block :: yaml

    staging:
        name: "myapp-staging"
        host: "localhost"
        port: 5432
        user: "test-user"
        pass: "password"
    production:
        name: "myapp-production"
        host: "54.21.35.141"
        port: 5432
        user: "user"
        pass: "password"

Access to the configuration is as follows:

.. code-block :: yaml

    from myapp.config import settings

    print settings.staging.host
    print settings.production.host

Configurations can be nested to any depth, but it is recommended to keep
them fairly shallow, to avoid deep accessor chains.
