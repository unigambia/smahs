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
        blank=True,
        related_name="lecturer",
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

class CourseMaterialQuerySet(models.QuerySet):
    def get_assignments(self):
        return self.filter(type="assignment")

    def get_lecture_notes(self):
        return self.filter(type="lecture_note")

    def get_past_questions(self):
        return self.filter(type="past_question")

    def get_other_materials(self):
        return self.filter(type="others")

class CourseMaterialManager(models.Manager):
    def get_queryset(self):
        return CourseMaterialQuerySet(self.model, using=self._db)

class CourseMaterial(models.Model):
    """Assignments"""
    CHOICES = (
        ("assignment", "Assignment"),
        ("lecture_note", "Lecture Note"),
        ("past_question", "Past Question"),
        ("others", "Others")
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="assignments", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    total_marks = models.IntegerField(default=0, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CHOICES, default="assignment")
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lecturer_assignment",
    )
    def __str__(self):
        return self.title

    objects = CourseMaterialManager()
   
    class Meta:
        ordering = ["-date_created"]

  