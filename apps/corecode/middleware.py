from .models import AcademicSession, AcademicSemester


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = AcademicSession.objects.get(current=True)
        current_semester = AcademicSemester.objects.get(current=True)

        request.current_session = current_session
        request.current_semester = current_semester

        response = self.get_response(request)

        return response
