[![Build Status](https://travis-ci.org/botswana-harvard/edc-identifier.svg?branch=develop)](https://travis-ci.org/botswana-harvard/edc-identifier)

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
