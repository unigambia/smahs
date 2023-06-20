from .models import AcademicSession, AcademicSemester, SiteConfig


def site_defaults(request):
    current_session = AcademicSession.objects.get(current=True)
    current_semester = AcademicSemester.objects.get(current=True)
    vals = SiteConfig.objects.all()
    contexts = {
        "current_session": current_session.name,
        "current_semester": current_semester.name,
    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts
