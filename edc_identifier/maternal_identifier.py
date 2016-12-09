from .infant_identifier import InfantIdentifier
from .subject_identifier import SubjectIdentifier
from .models import IdentifierModel


class MaternalIdentifierError(Exception):
    pass


class MaternalIdentifier(SubjectIdentifier):

    def __init__(self, **kwargs):
        self.infants = []
        self.study_site = kwargs.get('study_site')
        super(MaternalIdentifier, self).__init__(**kwargs)
        infant_identifiers = []
        for obj in IdentifierModel.objects.filter(linked_identifier=self.identifier).order_by('linked_identifier'):
            infant_identifiers.append(obj.identifier)
        if infant_identifiers:
            birth_order, live_infants = InfantIdentifier.reverse_infant_suffix(infant_identifiers[0])
            self.infants = [InfantIdentifier()] * live_infants
            for index, identifier in enumerate(infant_identifiers):
                birth_order, live_infants = InfantIdentifier.reverse_infant_suffix(infant_identifiers[index])
                self.infants[birth_order] = InfantIdentifier(identifier=identifier)

    @property
    def label(self):
        return 'maternalidentifier'

    def deliver(self, live_infants, model, birth_orders=None, create_registration=None, **kwargs):
        """Deliver all infants, only instantiate InfantIdentifier with maternal identifier
        if listed in birth orders or if birth orders is None."""
        create_registration = True if create_registration is None else create_registration
        if self.infants:
            raise MaternalIdentifierError(
                'Infant identifiers already created for this mother. Got {}'.format(self.infants))
        else:
            # birth order is zero-based, may be a list of strings, ints or none.
            if birth_orders:
                try:
                    birth_orders = [int(n) - 1 for n in birth_orders.split(',')]
                except AttributeError:
                    birth_orders = [n - 1 for n in birth_orders]
                if min(birth_orders) < 0 or max(birth_orders) >= live_infants:
                    raise MaternalIdentifierError(
                        'Invalid birth order list for live_infants == {}. Got {}'.format(live_infants, birth_orders))
            else:
                birth_orders = range(0, live_infants)
            for birth_order in range(0, live_infants):
                if birth_order in birth_orders:
                    self.infants.append(
                        InfantIdentifier(
                            maternal_identifier=self,
                            model=model,
                            birth_order=birth_order,
                            live_infants=live_infants,
                            create_registration=create_registration,
                            **kwargs))
                else:
                    # instantiate empty object
                    self.infants.append(InfantIdentifier())
