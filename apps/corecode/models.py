from django.db import models
from ..staffs.models import Staff
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User
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
    start_date = models.DateField()
    end_date = models.DateField()
    current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='session_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='session_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicSemester(models.Model):
    """Academic Semester"""

    name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, default=1)
    current = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='semester_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='semester_updated_by', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class StudentCohort(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='cohort_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='cohort_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_updated_by', null=True, blank=True, on_delete=models.SET_NULL)

    coordinator  = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinator",
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_registration_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_registration_updated_by', null=True, blank=True, on_delete=models.SET_NULL)


    class Meta:
        unique_together = ['student', 'course', 'academic_session', 'academic_semester']

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='course_material_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='course_material_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
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

  
class Exam(models.Model):
    """Exams"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="exams", null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    total_marks = models.IntegerField(default=0, null=True, blank=True)
    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    academic_semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    cohort = models.ForeignKey(StudentCohort, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    created_by = models.ForeignKey(User, related_name='exam_created_by', null=True, blank=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(User, related_name='exam_updated_by', null=True, blank=True, on_delete=models.SET_NULL)
    lecturer = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lecturer_exam",
    )
    def __str__(self):
        return self.title

    objects = CourseMaterialManager()
   
    class Meta:
        ordering = ["-date_created"]