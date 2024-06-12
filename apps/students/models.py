from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from apps.corecode.models import StudentCohort
from apps.corecode.models import Course
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save



class Student(models.Model):

    STATUS_CHOICES = [("active", "Active"), ("graduate", "Graduate ")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    year_enrolled = models.IntegerField(default=timezone.now().year)
    mat_number = models.CharField(max_length=200, unique=True)
    surname = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_cohort = models.ForeignKey(
        StudentCohort, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    is_cleared = models.BooleanField(default=False)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="student_created_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="student_updated_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.mat_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
    
@receiver(post_save, sender=Student)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.email # You can use the mat_number as the username
        password = "student@utg"  # Generate a random password
        user = User.objects.create_user(username=username, password=password)
        instance.user = user
        instance.save()


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
