from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicSemester,
    SiteConfig,
    StudentCohort,
    Course,
    CourseMaterial, 
    Exam,
    Department,
    Program,
    CourseRegistrationPeriod
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
        fields = ["name", "code", "credit_unit", "level", "coordinator", "program"]

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
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

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


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description', 'head']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['description'].widget.attrs['placeholder'] = 'Enter a brief description of the department'
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['description'].widget.attrs['cols'] = 40
        self.fields['description'].widget.attrs['class'] = 'form-control'


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'year_of_study', 'department']


class CourseRegistrationPeriodForm(ModelForm):

    class Meta:
        model = CourseRegistrationPeriod
        fields = ['start_date', 'end_date', 'status', 'academic_semester', 'academic_session']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        labels = {
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        help_texts = {
            'status': 'Select the status of the registration period',
        }
        error_messages = {
            'start_date': {
                'required': 'Please enter the start date of the registration period',
            },
            'end_date': {
                'required': 'Please enter the end date of the registration period',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('The start date cannot be greater than the end date.')

        return cleaned_data