# Shell to use with Make
SHELL := /bin/bash

# Set important Paths
PROJECT := confire
LOCALPATH := $(CURDIR)/$(PROJECT)
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

# Export targets not associated with files
.PHONY: test coverage pip clean uml build deploy install

# Clean build files
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	find . -name "__pycache__" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info
	-rm -rf .eggs
	-rm -rf site
	-rm -rf classes_$(PROJECT).png
	-rm -rf packages_$(PROJECT).png
	-rm -rf docs/_build

# Targets for Confire testing
test:
	python setup.py test
	make clean

# Draw UML diagrams
uml:
	pyreverse -ASmy -k -o png -p $(PROJECT) $(LOCALPATH)

# Build the universal wheel and source distribution
build:
	python setup.py sdist bdist_wheel

# Install the package from source
install:
	python setup.py install

# Deploy to PyPI
deploy:
	python setup.py register
	twine upload dist/*
