Examples
========

Consenting Subjects
-------------------

By default, :meth:`save` in the base consent model from module :mod:`consent` uses an instance of 
:class:`bhp_identifier.classes.Subject` to allocate an identifier to the consenting subject:

.. code-block:: python
   :emphasize-lines: 15-17   
    
    class BaseConsent(BaseSubject):
        
        ...

        def save(self, *args, **kwargs):
            """ create or get a subject identifier and update registered subject """
            subject = Subject()
            registered_subject = getattr(self, 'registered_subject', None)
            if not self.id:
                # see if there is a registered subject key. want to know this as it
                # might have the subject identifier already (e.g for subjects re-consenting)
                if registered_subject:
                    # set identifier, but it may be None
                    self.subject_identifier = self.registered_subject.subject_identifier
                if not self.subject_identifier:  
                    # allocate new subject identifier
                    self.subject_identifier = subject.get_identifier(self.get_subject_type(),
                                                                 self.study_site.site_code)
            # call super
            super(BaseConsent, self).save(*args, **kwargs) 
            # create or update RegisteredSubject
            subject.update_register(self, 
                                    subject_identifier = self.subject_identifier,
                                    registration_datetime = self.created,
                                    registration_status = 'consented',
                                    subject_consent_id = self.pk)


Infants
-------
To register infants for an already registered mother add the following to the save method of the ModelAdmin. 
For example, using the Maternal Delivery form, create an instance of :class:`bhp_identifier.classes.Infant` and call it's 
:meth:`bhp_identifier.classes.Infant.get_identifier` method::

    class MaternalLabDelAdmin(MaternalVisitModelAdmin):
        
        ...
        
        def save_model(self, request, obj, form, change):
         
                if not change:
                    obj.user_created = request.user
                    obj.save()
                    if obj.live_infants_to_register > 0:
                        #Allocate Infant Identifier
                        infant=Infant()
                        infant.get_identifier(request.user, 
                                  maternal_identifier = obj.maternal_visit.appointment.registered_subject.subject_identifier,
                                  maternal_study_site = obj.maternal_visit.appointment.registered_subject.study_site,
                                  live_infants = obj.live_infants,
                                  live_infants_to_register = obj.live_infants_to_register,
                                  subject_type='infant',
                                  )
                return super(MaternalLabDelAdmin, self).save_model(request, obj, form, change)