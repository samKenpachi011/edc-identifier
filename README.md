<!-- [![Build Status](https://travis-ci.org/clinicedc/edc-identifier.svg?branch=develop)](https://travis-ci.org/clinicedc/edc-identifier)
[![Coverage Status](https://coveralls.io/repos/clinicedc/edc-identifier/badge.svg)](https://coveralls.io/r/clinicedc/edc-identifier) -->
[![Build Status](https://app.travis-ci.com/samKenpachi011/edc-identifier.svg?branch=develop)](https://app.travis-ci.com/samKenpachi011/edc-identifier)

<!-- [![Coverage Status](https://coveralls.io/repos/github/samKenpachi011/edc-identifier/badge.svg?branch=develop)](https://coveralls.io/github/samKenpachi011/edc-identifier?branch=develop) -->
[![Coverage Status](https://coveralls.io/repos/github/samKenpachi011/edc-identifier/badge.svg?branch=develop&cache=buster)](https://coveralls.io/github/samKenpachi011/edc-identifier?branch=develop)


[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/samKenpachi011/edc-identifier/releases/tag/v1.0.0)
[![Log Scan Status](https://img.shields.io/badge/Log%20Scan-Passing-brightgreen.svg)](https://app.travis-ci.com/github/samKenpachi011/edc-identifier/logscans)



# edc-identifier

Add research subject identifiers and other useful identifiers to your project

## Installation

Add to settings:

    INSTALLED_APPS = [
        ...
        'edc_identifier.apps.AppConfig',
        ...
    ]

## Identifiers for research subjects

### Subject Identifiers

For example:

    from edc_identifier.subject_identifier import SubjectIdentifier

    subject_identifier = SubjectIdentifier(
        subject_type_name='subject',
        model='edc_example.enrollment',
        protocol='000',
        device_id='99',
        study_site='40')
    >>> subject_identifier.identifier
    '000-40990001-6'


### Maternal and Infant Identifiers

See also, `edc_pregnancy` model mixins `DeliveryMixin`, `BirthMixin`.

For example:

    from edc_identifier.maternal_identifier import MaternalIdentifier

    maternal_identifier = MaternalIdentifier(
        subject_type_name='maternal',
        model='edc_example.enrollment',
        study_site='40',
        last_name='Carter')

    >>> maternal_identifier.identifier
    '000-40990001-6'

Add infants

    >>> maternal_identifier.deliver(2, model='edc_example.maternallabdel')
    >>> [infant.identifier for infant in maternal_identifier.infants]
    ['000-40990001-6-25', '000-40990001-6-26']

`maternal_identifier.infants` is a list of `InfantIdentifier` instances

Reload class:

    >>> maternal_identifier = MaternalIdentifier(identifier='000-40990001-6')
    >>> maternal_identifier.identifier
    '000-40990001-6'
    >>> [infant.identifier for infant in maternal_identifier.infants]
    ['000-40990001-6-25', '000-40990001-6-26']

Only allocate an identifier to one infant of twins:

    >>> maternal_identifier.deliver(2, model='edc_example.maternallabdel', birth_orders='2')
    >>> [infant.identifier for infant in maternal_identifier.infants]
    [None, '000-40990001-6-26']

Of triplets, allocate identifiers to the 2nd and 3rd infants only:

    >>> maternal_identifier.deliver(3, model='edc_example.maternallabdel', birth_orders='2,3')
    >>> [infant.identifier for infant in maternal_identifier.infants]
    [None, '000-40990001-6-37', '000-40990001-6-38']


## Research subject identifier classes can create a Registered Subject instance

See also `edc_registration`

`SubjectIdentifier` by default does not create a `RegisteredSubject` instance unless `create_registration=True`.

By default, `MaternalIdentifier` and `InfantIdentifier` create `RegisteredSubject` instances that can be updated with full details later with the Delivery and Birth models. Continuing from above:

    maternal_identifier = MaternalIdentifier(identifier='000-40990001-6')
    maternal_identifier.deliver(1, model='edc_example.maternallabdel', create_registration=True)

    # mother
    >>> RegisteredSubject.objects.get(subject_identifier='000-40990001-6')
    <RegisteredSubject '000-40990001-6'>

    # infant is linked to the mother
    >>> RegisteredSubject.objects.get(linked_identifier='000-40990001-6')
    <RegisteredSubject '000-40990001-6-10'>

    # infant
    >>> obj = RegisteredSubject.objects.get(subject_identifier='000-40990001-6-10')
    >>> obj.first_name
    'Baby1Carter'  ## generates a temp name until Birth form is added with complete information.
    >>> obj.relative_identifier
    '000-40990001-6'


### Subject type "Caps" are enforced by the research subject identifier classes

See also `edc_protocol`

Limits on the number of identifiers that can be allocated per subject type are enforced when identifiers are created. `edc_identifier` reads the "caps" from `edc_protocol.apps.AppConfig` linking the subject type, e.g. `subject`, or `maternal` or `infant`, to the relevant cap and not allowing the number of allocated identifiers to exceed the cap.

## Base classes for identifiers.

### Numeric Identifiers

The numeric identifier uses a check-digit and may have a separator if specified.

	from edc_identifier import NumericIdentifier

	class MyIdentifier(NumericIdentifier):
		pass

	>>> id = MyIdentifier(None)
	>>> id
	MyIdentifier('00000000018')
	>>> next(id)
	'00000000026'
	>>> next(id)
	'00000000034'


	# add a separator
	class MyIdentifier(NumericIdentifier):
    	identifier_pattern = r'^[0-9]{4}\-[0-9]{4}\-[0-9]{4}$'
    	checkdigit_pattern = r'^\-[0-9]{1}$'
    	separator = '-'
    	seed = ['3200-0000-0000']

	>>> id = MyIdentifier(None)
	>>> id
	MyIdentifier('3200-0000-0001-1')
	>>> next(id)
	'3200-0000-0002-9'
	>>> next(id)
	'3200-0000-0003-7'

	# start from the last identifier, increment is immediate and automatic
	>>> id = MyIdentifier('3200-0000-3222-0')
	>>> id
	MyIdentifier('3200-0000-3223-8')


### Alphanumeric Identifiers

	from edc_identifier import AlphanumericIdentifier

	class MyIdentifier(AlphanumericIdentifier):
		alpha_pattern = r'^[A-Z]{3}$'
		numeric_pattern = r'^[0-9]{4}$'
		seed = ['AAA', '0000']

	>>> id = MyIdentifier(None)
	>>> id
	MyIdentifier('AAA00015')

Your identifier will starts with 'AAA0001' plus the checkdigit "5". Subsequent calls to next increment like this:

	>>> print(next(id))
	AAA00023
	>>> print(next(id))
	AAA00031
	>>> print(next(id))
	AAA00049


The identifier increments on the numeric sequence then the alpha:

	>>> id = MyIdentifier('AAA99991)
	>>> id
	MyIdentifier('AAB00013')

	>>> next(id)
	'AAB00021'
	>>> next(id)
	'AAB00039'
	>>> next(id)
	'AAB00047'

	>>> id = MyIdentifier('AAB99999')
	>>> id
	MyIdentifier('AAC00010')
	...

See `getresults-receive` for sample usage with `settings` and a `History` model.

### Short Identifiers

Creates a small identifier that is almost unique, for example, across 25 Edc devices in a community. We use these as sample requisition identifiers that are transcribed manually onto a tube from the Edc screen in a household. Once the sample is received at the local lab it is allocated a laboratory-wide unique specimen identifier.

    from edc_identifier import ShortIdentifier

    >>> ShortIdentifier()
    ShortIdentifier('46ZZ2')

Add a static prefix -- prefix(2) + identifier(5):

	from edc_identifier import ShortIdentifier

	class MyIdentifier(ShortIdentifier):
    	prefix_pattern = r'^[0-9]{2}$'

    >>> options = {'prefix': 22}
    >>> id = MyIdentifier(options=options)
	>>> id
	MyIdentifier('22UYMBT')
	>>> next(id)
	'22KM84G'

Add a checkdigit -- prefix(2) + identifier(5) + checkdigit(1):

	from edc_identifier import ShortIdentifier

	class MyIdentifier(ShortIdentifier):
    	prefix_pattern = r'^[0-9]{2}$'
    	checkdigit_pattern = r'^[0-9]{1}$'

    >>> options = {'prefix': 22}
    >>> id = MyIdentifier(options=options)
	>>> id
	MyIdentifier('223GF8A3')
	>>> next(id)
	'22DXVW23'

We use this in edc-quota to get a confirmation code:

	from edc_identifier import ShortIdentifier

	class ConfirmationCode(ShortIdentifier):

	    identifier_type = 'confirmation'
	    prefix_pattern = ''

	>>> code = ConfirmationCode()
	>>> print(code)
	CAT33
	>>> next(code)
	3FU7D

Add more to the prefix, such as device code and community code.

	from edc_identifier.short_identifier import ShortIdentifier

	class RequisitionIdentifier(ShortIdentifier):

		identifier_type = 'requisition'
		prefix_pattern = r'^[0-9]{4}$'
		template = '{device_id}{community_id}{random_string}'

		@property
		def options(self):
			if 'prefix' not in self._options:
				self._options.update(
					{'prefix': str(self._options.get('device_id')) + str(self._options.get('community_id'))})
			return self._options

    >>> options = {'device_id': 22, 'community_id': '12'}
    >>> id = RequisitionIdentifier(options=options)
	>>> id
	RequisitionIdentifier('22126MZXD')
	>>> next(id)
	'2212Y899C'

... if you prefer not to use the `IdentifierHistory` model, for example, if you are filling in a model field on save():

	from my_app.models import Requisition

	class RequisitionIdentifier(ShortIdentifier):

	    identifier_type = 'requisition'
	    requisition_model = Requisition

	    def is_duplicate(self, identifier):
	        try:
	            self.requisition_model.get(requisition_identifier=identifier)
	            return True
	        except self.requisition_model.DoesNotExist:
	            pass
	        return False

		def update_history(self):
			pass


### Batch Identifier

To have an identifier prefixed by the current date stamp:

	from edc_identifier.batch_identifier import BatchIdentifier

	>>> datetime.today().strftime('%Y%m%d)
	20150817
	>>> id = BatchIdentifier()
	>>> id
	BatchIdentifier('201508170001')
	>>> next(id)
	'201508170002'
