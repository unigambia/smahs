from django.db import models
from django.utils import timezone

class AdmissionCycle(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    Created_by = models.CharField(max_length=255, default='None')
    Updated_by = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.name

class AdmissionApplication(models.Model):
    admission_cycle = models.ForeignKey(AdmissionCycle, on_delete=models.CASCADE, related_name='applications')
    applicant_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    application_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
    Created_by = models.CharField(max_length=255, default='None')
    Updated_by = models.CharField(max_length=255, default='None')

    def __str__(self):
        return self.applicant_name
