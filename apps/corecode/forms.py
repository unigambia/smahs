from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
)

SiteConfigForm = modelformset_factory(
    SiteConfig,
    fields=(
        "key",
        "value",
    ),
    extra=0,
)


class AcademicSessionForm(ModelForm):
    prefix = "Academic Session"

    class Meta:
        model = AcademicSession
        fields = ["name", "current"]


class AcademicSemesterForm(ModelForm):
    prefix = "Academic Semester"

    class Meta:
        model = AcademicSemester
        fields = ["name", "current"]


class CourseForm(ModelForm):
    prefix = "Course"

    class Meta:
        model = Course
        fields = ["name"]


class StudentCohortForm(ModelForm):
    prefix = "Cohort"

    class Meta:
        model = StudentCohort
        fields = ["name"]


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_semester = forms.ModelChoiceField(
        queryset=AcademicSemester.objects.all(),
        help_text='Click <a href="/semester/create/?next=current-session/">here</a> to add new semester',
    )
