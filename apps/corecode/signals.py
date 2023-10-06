from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AcademicSession, AcademicSemester, Course, CourseMaterial, Exam, StudentCohort, StudentCourse
from .current_user import get_current_user

@receiver(post_save, sender=AcademicSession)
def after_saving_session(sender, created, instance, *args, **kwargs):
    """Change all academic sessions to false if this is true"""
    if instance.current is True:
        AcademicSession.objects.exclude(pk=instance.id).update(current=False)
    
@receiver(pre_save, sender=AcademicSession)
def session_pre_save(sender, instance, **kwargs):
    # This signal runs before a Session is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

 
@receiver(post_save, sender=AcademicSemester)
def after_saving_semester(sender, created, instance, *args, **kwargs):
    """Change all academic semesters to false if this is true."""
    if instance.current is True:
        AcademicSemester.objects.exclude(pk=instance.id).update(current=False)

@receiver(pre_save, sender=AcademicSemester)
def semester_pre_save(sender, instance, **kwargs):
    # This signal runs before a Semester is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

@receiver(pre_save, sender=Course)
def course_pre_save(sender, instance, **kwargs):
    # This signal runs before a Course is saved.
    if not instance.pk:  # Checking if object is new
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

@receiver(pre_save, sender=CourseMaterial)
def course_material_pre_save(sender, instance, **kwargs):
    # This signal runs before a CourseMaterial is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

@receiver(pre_save, sender=Exam)
def exam_pre_save(sender, instance, **kwargs):
    # This signal runs before a Exam is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

@receiver(pre_save, sender=StudentCohort)
def student_cohort_pre_save(sender, instance, **kwargs):
    # This signal runs before a StudentCohort is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()

@receiver(pre_save, sender=StudentCourse)
def student_course_pre_save(sender, instance, **kwargs):
    # This signal runs before a StudentCourse is saved.
    if not instance.pk:
        instance.created_by = get_current_user()
    instance.updated_by = get_current_user()