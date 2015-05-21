Installation
============

Checkout:: 

    http://192.168.1.50/svn/bhp_identifier
    
Add to settings::

    INSTALLED_APPS={
        
        ...
        
        'bhp_identifier',
        
        ...    
    }    
    
    PROJECT_IDENTIFIER_PREFIX = '056' # default identifier prefix 
                                      # if keyword 'prefix' in identifier format     
    PROJECT_IDENTIFIER_MODULUS = 7 # (default)
    
    # only specify if other than the default
    # see Base.get_identifier() for available keys and current 
    # default identifier formats
    # format is {identifier_type: format}
    # !!! not yet implemented !!!
    # IDENTIFIER_FORMATS = { 
    #    'subject': '{prefix}-{site}{device_id}{sequence}'
    #    'requisition': ''{prefix}{site}{device_id}{sequence}'
    #    'specimen': ''{prefix}{site}{device_id}{sequence}'
    E    }