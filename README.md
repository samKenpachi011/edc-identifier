[![Build Status](https://travis-ci.org/botswana-harvard/edc-identifier.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-identifier)
[![Coverage Status](https://coveralls.io/repos/botswana-harvard/edc-identifier/badge.svg)](https://coveralls.io/r/botswana-harvard/edc-identifier)
[![Documentation Status](https://readthedocs.org/projects/django-crypto-fields/badge/?version=latest)](https://readthedocs.org/projects/edc-identifier/?badge=latest)
[![PyPI version](https://badge.fury.io/py/edc-identifier.svg)](http://badge.fury.io/py/edc-identifier)
[![Code Health](https://landscape.io/github/botswana-harvard/edc-identifier/master/landscape.svg?style=flat)](https://landscape.io/github/botswana-harvard/edc-identifier/master)
# edc-identifier
Manage identifier creation in the Edc

Installation
------------

	pip install edc-identifier

Add to settings:

	# modulus to calculate check digit
	IDENTIFIER_MODULUS = 7
	# prefix for all participant identifiers
	IDENTIFIER_PREFIX = '066'
