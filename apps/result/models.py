from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicSemester,
    StudentCohort,
    Course,
)
from apps.students.models import Student

from .utils import score_grade, grade_point


# Create your models here.
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    semester = models.ForeignKey(AcademicSemester, on_delete=models.CASCADE)
    current_cohort = models.ForeignKey(StudentCohort, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["course"]

    def __str__(self):
        return f"{self.student} {self.session} {self.semester} {self.course}"

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())
    
    def gpa(self):
        return grade_point(self.grade())
