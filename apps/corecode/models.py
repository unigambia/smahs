from django.db import models
from ..staffs.models import Staff
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    name = models.CharField(max_length=200, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicSemester(models.Model):
    """Academic Semester"""

    name = models.CharField(max_length=20, unique=True)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class StudentCohort(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Cohort"
        verbose_name_plural = "Cohorts"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    """Course"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True , null=True)
    credit_unit = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    lecturer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'academic'}
    )
    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class StudentCourse(models.Model):
    from apps.students.models import Student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student can't register for the same course twice

    # def __str__(self):
    #     return f"{self.student.surname} registered for {self.course.name} on {self.registration_date} in {self.academic_session}"