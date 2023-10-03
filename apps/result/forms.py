from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicSemester, Course

from .models import Result


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
        fields = ["student", "session", "semester", "course", "test_score", "exam_score"]
