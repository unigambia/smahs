from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicSemester,
    StudentCohort,
    Course,
    Exam
)
from apps.students.models import Student
from django.contrib.auth.models import User

from .utils import score_grade, grade_point


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name="result_created_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        related_name="result_updated_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )


    class Meta:
        ordering = ["course"]
        unique_together = ['student', 'session', 'semester', 'course']


    def __str__(self):
        return f"{self.student} {self.session} {self.semester} {self.course}"

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())
    
    def gpa(self):
        return grade_point(self.grade())

