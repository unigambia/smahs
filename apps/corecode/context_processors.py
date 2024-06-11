from .models import AcademicSession, AcademicSemester, SiteConfig


def site_defaults(request):
    try:
        current_session = AcademicSession.objects.get(current=True)
        current_session_name = current_session.name
    except AcademicSession.DoesNotExist:
        current_session_name = None

    try:
        current_semester = AcademicSemester.objects.get(current=True)
        current_semester_name = current_semester.name
    except AcademicSemester.DoesNotExist:
        current_semester_name = None

    vals = SiteConfig.objects.all()
    contexts = {
        "current_session": current_session_name,
        "current_semester": current_semester_name,
    }

    for val in vals:
        contexts[val.key] = val.value

    return contexts
