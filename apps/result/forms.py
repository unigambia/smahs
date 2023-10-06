from django import forms
from django.forms import modelformset_factory, ValidationError

from apps.corecode.models import AcademicSession, AcademicSemester, Course

from .models import Result
from apps.corecode.models import StudentCourse


class CreateResults(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    semester = forms.ModelChoiceField(queryset=AcademicSemester.objects.all())
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple
    )


EditResults = modelformset_factory(
    Result, fields=("test_score", "exam_score"), extra=0, can_delete=True
)

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["student", "session", "semester", "course","exam", "test_score", "exam_score"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student = self.data.get('student')
        session = self.data.get('session')
        semester = self.data.get('semester')

        if student and session and semester:
                    registrations = StudentCourse.objects.filter(student_id=student, academic_session_id=session, academic_semester_id=semester)
                    self.fields['course'].queryset = Course.objects.filter(id__in=registrations.values_list('course_id'))

    def clean_course(self):
        course = self.cleaned_data.get('course')
        student = self.cleaned_data.get('student')
        session = self.cleaned_data.get('session')
        semester = self.cleaned_data.get('semester')

        if student and session and semester:
            registrations = StudentCourse.objects.filter(student_id=student, academic_session_id=session, academic_semester_id=semester)
            valid_courses = Course.objects.filter(id__in=registrations.values_list('course_id'))
            if course not in valid_courses:
                raise ValidationError("Invalid course selection for the given student, session, and semester.")
        
        return course
                