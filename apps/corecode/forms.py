from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
    CourseMaterial, 
    Exam
)

from django.contrib.auth.models import User

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
        fields = ["name", "current", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class AcademicSemesterForm(ModelForm):
    prefix = "Academic Program"

    class Meta:
        model = AcademicSemester
        fields = ["name", "current", "start_date", "end_date", "session"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class CourseForm(ModelForm):
    # prefix = "Course"

    class Meta:
        model = Course
        fields = ["name", "code", "credit_unit", "level", "coordinator"]

class AssignmentForm(ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ["title", "due_date", "description", "file", "total_marks"]

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].widget = forms.DateInput(attrs={'type': 'date'})

class UserForm(ModelForm):
    prefix = "User"

    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_superuser", "first_name", "last_name", "password",]

class RegistrationForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()

    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

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


class ExamForm(ModelForm):
    class Meta:
            model = Exam
            fields = '__all__'
            
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['due_date'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['date_created'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
