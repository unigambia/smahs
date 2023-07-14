from django.db import models
from ..staffs.models import Staff
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
