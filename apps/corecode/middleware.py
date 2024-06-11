from .models import AcademicSession, AcademicSemester
import threading

_thread_locals = threading.local()

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_session = AcademicSession.objects.get(current=True)
        except AcademicSession.DoesNotExist:
            current_session = None
        
        try:
            current_semester = AcademicSemester.objects.get(current=True)
        except AcademicSemester.DoesNotExist:
            current_semester = None
        
        request.current_session = current_session
        request.current_semester = current_semester
        response = self.get_response(request)
        return response


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = getattr(request, 'user', None)
        return self.get_response(request)
