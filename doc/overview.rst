Overview
========

:mod:`bhp_identifier` is a module to handle identifier allocation for various subject types. An identifier is created as follows:
    * from ModelAdmin.save_model() or Model.save() call :func:`get_identifier` of a selected bhp_identifier class, e.g :class:`SubjectIdentifier`.
    * identifier class combines the device_id from :mod:`settings.py` and a sequence number from model :class:`Sequence` to create a unique
      identifier.
      
The models involved are:
    * :class:`models.subject_identifier.SubjectIdentifier`
    * :class:`Sequence`
    
Also, the settings attribute DEVICE_ID is required for each device that creates identifiers. 

.. warning:: If more than one device creates identifiers ensure the DEVICE_ID for each device is unique 
             and that the model :class:`Sequence` is maintained on that device.