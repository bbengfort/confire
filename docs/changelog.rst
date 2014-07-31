.. Confire documentation file, created by Benjamin Bengfort on Wed Jul 30 20:13:44 2014.

Changelog
=========

The release versions that are sent to the Python package index are also tagged in Github. You can see the tags through the Github web application and download the tarball of the version you'd like. Additionally PyPI will host the various releases of confire.

The versioning uses a three part version system, "a.b.c" - "a" represents a major release that may not be backwards compatible. "b" is incremented on minor releases that may contain extra features, but are backwards compatible. "c" releases are bugfixes or other micro changes that developers should feel free to immediately update to.

Contributors
------------

I'd like to personally thank the following people for contributing to confire and making it a success!

- `@tyrannosaurus <https://github.com/tyrannosaurus>`_
- `@murphsp1 <https://github.com/murphsp1>`_
- `@keshavmagge <https://github.com/keshavmagge>`_
- `@ojedatony1616 <https://github.com/ojedatony1616>`_

Versions
--------

The following lists the various versions of confire and important details about them.

v0.2.0
~~~~~~

* **tag**: v0.2.0
* **deployment**: July 31, 2014
* **commit**: (latest)

This release added some new features including support for environmental variables as settings defaults, ConfigurationMissing Warnings and ImproperlyConfigured errors that you can raise in your own code to warn developers about the state of configuration.

This release also greatly increased the amount of available documentation for Confire.

v0.1.1
~~~~~~

* **tag**: v0.1.1
* **deployment**: July 24, 2014
* **commit**: bdc0488

Added Python 3.3 support thanks to `@tyrannosaurus <https://github.com/tyrannosaurus>`_ who contributed to the changes that would ensure this support for the future. I also added Python 3.3 travis testing and some other minor changes.

v0.1.0
~~~~~~

* **tag**: v0.1.0
* **deployment**: July 20, 2014
* **comit**: 213aa5e

Initial deployment of the confire library.

