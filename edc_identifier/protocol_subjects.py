from django.conf import settings

if settings.APP_NAME == 'edc_identifier':

    from edc_protocol.subject_type import SubjectType
    from edc_protocol.site_protocol_subjects import site_protocol_subjects

    subject = SubjectType(
        name='subject',
        verbose_name='Research Subjects',
        model='edc_identifier.enrollment')

    subject.add_enrollment_cap(site=None, max_subjects=9999)

    site_protocol_subjects.register(subject)

    subject = SubjectType(
        name='subject',
        verbose_name='Research Subjects',
        model='edc_identifier.enrollmentthree')

    subject.add_enrollment_cap(site=None, max_subjects=5)

    site_protocol_subjects.register(subject)
