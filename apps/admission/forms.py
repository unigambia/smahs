from django import forms
from .models import AdmissionCycle, AdmissionApplication

class AdmissionCycleForm(forms.ModelForm):
    class Meta:
        model = AdmissionCycle
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = ['admission_cycle', 'applicant_name', 'date_of_birth', 'email', 'phone_number', 'address', 'status']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
